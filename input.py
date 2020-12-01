import os


def get_lines(file_):
    if os.path.isfile(file_) and os.path.exists(file_):
        with open(file_, newline=None) as f:
            lines = f.readlines()
            return lines
    else:
        print(f'Input file is incorrect! Check file is valid and try again.\n>>>\t{file_}')


def get_input_file(py_file):
    if os.path.isfile(py_file) and os.path.exists(py_file):
        base = os.path.splitext(py_file)[0]
        return ''.join([base, '_input', '.txt'])
