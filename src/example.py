#: # Example
#: This is an example file to show the capabilities of the format.

#: ## The basics
#: This section shows the basics of the format.

#: ### Code cells
#: You can write regular python source in here:
print('Hello, World!')

#: As you can see, the code gets converted into notebook code cells.
#: The output of the cell is also included if you run the converter with the `-e` flag.

#: And you have probably already noticed that you can insert Markdown cells.

#: ### Markdown cells
#: To create a Markdown cell, you need to write a special comment starting with `#: `.
#:
#:     #: ### This will be a Markdown header
#:     print('Hello from a code cell!')

#: ### Regular comments
#: You can still write regular comments as well, just don't put the `:` right after the `#` sign:
# This will be a regular comment inside a code cell!

#: ### Big code cells
#: Multiple lines of code in a row are merged into one code cell, even including empty lines!

print('This is the first line')
print('Hello from the second line!')

print('This is the line #4 from the same code cell')

#: ### Several code cells in a row
#: If you need to break a big chunk of code up into multiple cells,
#: you can do so by putting a special "separator" comment `#=`:
# This is a cell
#=
# And this is another one
#=
# And this is the third one


#: ## The Markdown
#: You can do many things with markdown, but this section does not aim to show any existing or even supported feature.
#: Instead, this section describes some important things to note when writing markdown comments in this format.

#: ### Headers
#: This one may seem obvious, but you should put a space after the sequence of `#`s, otherwise the header may be interpreted as something else.
#:
#:     #: #### Right
#:     #: ####Wrong

#: ### Tables
#: Tables require an empty line before before the first row if there is some text above in the same cell,
#: otherwise they are not interpreted correctly and things get messy:
#:
#:     #: Right:
#:     #:
#:     #: | A | B | C |
#:     #: |:--|:-:|--:|
#:     #: | 1 | 2 | 3 |
#:
#:     #: Wrong:
#:     #: | A | B | C |
#:     #: |:--|:-:|--:|
#:     #: | 1 | 2 | 3 |

#: ### Monospace blocks
#: As with tables, the multiline code blocks require nothing or an empty line right above,
#: otherwise they will be treated as inline ones.
#:
#:     #: Right:
#:     #:
#:     #:     Line one
#:     #:     Line two
#:     #:     Line three
#:
#:     #: Wrong:
#:     #:     Line one
#:     #:     Line two
#:     #:     Line three

#: ### TODO: This section should be expanded.


#: ## Evaluation
#: ### The basics
#: Code cells are evaluated one-by-one in a sequential order.
#: Output of every executed code cell gets printed right after the cell itself.

#: ### Exception handling
#: If an exception occurs during the execution of a cell, the traceback is printed to its `stderr` output, and the execution is aborted.
#: No subsequent cells get evaluated after that.
raise Exception('This is the end')
#=
print('But maybe not? Please...')
#: And currently this behaviour cannot be altered.

#: The `exit()` calls are treated almost the same way,
#: but instead of traceback the `[Interpreter finished execution with code {code}]` gets printed.
