import sys
from contextlib import redirect_stdout, redirect_stderr


template_file_path = 'ipynb_template.json'


def main(options):
    import json
    import os

    json_path = os.path.join(os.path.dirname(__file__), template_file_path)
    with open(json_path, 'r', encoding = 'utf8') as json_file:
        notebook = json.load(json_file)

    with open(options['input'], 'r', encoding = 'utf8') as input_file:
        notebook['cells'] = parse_cells(input_file.read())

    if options['evaluate']:
        evaluate_cells(notebook['cells'])

    with open(options['output'], 'w', encoding = 'utf8') as output_file:
        json.dump(notebook, output_file, indent = 1, sort_keys = True)



def evaluate_cells(cells):
    sandbox = create_sandboxed_context()
    for cell in cells:
        if cell['cell_type'] == 'code':
            if not update_cell_outputs(cell, sandbox):
                break


def update_cell_outputs(cell, context):
    cell['execution_count'] += 1

    with redirect_stdout(CellOutputsLogger(cell, 'stdout')), redirect_stderr(CellOutputsLogger(cell, 'stderr')):
        try:
            exec(compile(''.join(cell['source']), '<cell>', 'exec'), context)
        except SystemExit as ex:
            print('[Interpreter finished execution with code {}]'.format(ex.code or 0), file = sys.stderr)
            return False
        except Exception as err:
            import traceback
            traceback.print_exception(type(err), err, err.__traceback__.tb_next)
            return False

    return True


def create_sandboxed_context():
    context = {}
    exec('', context)
    return context


def parse_cells(text):
    cells = []

    prev_type = None
    for line in text.splitlines(keepends = False):
        if line.startswith('#='):
            prev_type = None
            continue
        elif line.startswith('#:'):
            if prev_type != 'markdown':
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": []
                })
                prev_type = 'markdown'
            cells[-1]['source'].append(line[3:] + '\n')
        else:
            if prev_type != 'code':
                cells.append({
                    'cell_type': 'code',
                    'execution_count': 0,
                    'metadata': {},
                    'outputs': [],
                    'source': []
                })
                prev_type = 'code'
            cells[-1]['source'].append(line + '\n')

    for i in range(len(cells) - 1, 0, -1):
        source = cells[i]['source']

        while len(source) > 0 and source[0].replace(' ', '') == '\n':
            del source[0]
        while len(source) > 0 and source[-1].replace(' ', '') == '\n':
            del source[-1]

        if not source:
            del cells[i]

    return cells


def parse_args(args):
    if not args:
        raise Exception('Argument list is empty')

    options = {
        'script': args[0],
        'evaluate': False,
        'debug': False
    }

    if len(args) < 2:
        return {}

    expected_option = ''
    for i in range(1, len(args)):
        arg = args[i]

        if expected_option:
            options[expected_option] = arg
            expected_option = ''
        elif arg.startswith('-'):
            flag = arg[1:]
            if flag in ['h', '-help']:
                return {}
            elif flag in ['o', '-output']:
                expected_option = 'output'
            elif flag in ['e', '-evaluate']:
                options['evaluate'] = True
            elif flag in ['d', '-debug']:
                options['debug'] = True
            else:
                raise Exception('Unexpected option: %s' % arg)
        else:
            if 'input' in options:
                raise Exception('Converting multiple input files is not supported')
            options['input'] = arg

    if expected_option:
        raise Exception('Expected argument for option "%s"' % expected_option)

    if not 'input' in options:
        raise Exception('No input file provided')

    if not 'output' in options:
        options['output'] = os.path.splitext(options['input'])[0] + '.ipynb'

    return options


def print_usage(script_name):
    print('Usage: python %s [-h] [-d] [-e] [-o <OUTPUT_FILE>] <INPUT_FILE>' % script_name)
    print('Options:')
    print('    -d, --debug:    Print traceback on errors')
    print('    -e, --evaluate: Execute the contents of code blocks sequentially in a sandboxed context and store the output')
    print('    -h, --help:     Show this help and exit')
    print('    -o, --output:   Specify the output filename. Default: same as INPUT_FILE, but .ipynb instead of .py')


class CellOutputsLogger:
    def __init__(self, cell, name):
        self.cell = cell
        self.name = name

    def write(self, text):
        outputs = self.cell['outputs']
        if not outputs or outputs[-1]['name'] != self.name:
            outputs.append({
                'name': self.name,
                'output_type': 'stream',
                'text': []
            })

        output_lines = outputs[-1]['text']
        new_lines = text.splitlines(keepends = True)
        if output_lines and not output_lines[-1].endswith('\n'):
            output_lines[-1] += new_lines.pop(0)

        output_lines += new_lines

    def flush(self):
        # FIXME: Flushing may actually be important in some cases.
        pass


if __name__ == '__main__':
    import sys
    
    try:
        options = parse_args(sys.argv)
    except Exception as err:
        print(err)
        exit(1)

    if not options:
        print_usage(sys.argv[0])
        exit(0)

    try:
        main(options)
    except Exception as err:
        print(err)
        if options['debug']:
            import traceback
            print('Debug details:')
            traceback.print_exc()
        exit(1)
