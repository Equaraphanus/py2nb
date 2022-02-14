def main(options):
    import json
    import os

    with open(options['input'], 'r', encoding = 'utf8') as input_file:
        notebook = json.load(input_file)

    with open(options['output'], 'w', encoding = 'utf8') as output_file:
        dump_as_python(notebook, output_file)


def dump_as_python(notebook, output_file):
    prev_type = None

    for cell in notebook['cells']:
        cell_type = cell['cell_type']
        source = cell.get('source')

        if cell_type == 'code':
            if cell_type == prev_type:
                print('\n#=', file = output_file)
            output_file.write(''.join(source))
        elif cell_type == 'markdown':
            lines = ''.join(source).splitlines()
            if prev_type != None:
                print('', file = output_file)
            for line in lines:
                print('#: %s' % line if line else '#:', file = output_file)
        else:
            print('Unknown cell type: %s' % cell_type)
            continue

        prev_type = cell_type


def parse_args(args):
    if not args:
        raise Exception('Argument list is empty')

    options = {
        'script': args[0],
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
        options['output'] = os.path.splitext(options['input'])[0] + '.py'

    return options


def print_usage(script_name):
    print('Usage: python %s [-h] [-d] [-o <OUTPUT_FILE>] <INPUT_FILE>' % script_name)
    print('Options:')
    print('    -d, --debug:    Print traceback on errors')
    print('    -h, --help:     Show this help and exit')
    print('    -o, --output:   Specify the output filename. Default: same as INPUT_FILE, but .ipynb instead of .py')


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
