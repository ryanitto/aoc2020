import os

INPUT_KEY = 'input'
TXT_SUFFIX = 'txt'

def get_lines(file_):
    if os.path.isfile(file_) and os.path.exists(file_):
        with open(file_) as f:
            lines = ''.join(f.readlines()).splitlines()
            return lines
    else:
        print(f'Input file is incorrect! Check file is valid and try again.\n>>>\t{file_}')


def get_input_file(py_file):
    shared_input_for_day = os.path.join(os.path.dirname(py_file), INPUT_KEY + f'.{TXT_SUFFIX}')

    if os.path.isfile(shared_input_for_day) and os.path.exists(shared_input_for_day):
        return shared_input_for_day

    if os.path.isfile(py_file) and os.path.exists(py_file):
        base = os.path.splitext(py_file)[0]
        return ''.join([base, f'_{INPUT_KEY}', f'.{TXT_SUFFIX}'])
