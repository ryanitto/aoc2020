"""
--- Day 2: Password Philosophy ---

Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we
can't log in!" You ask if you can take a look.

Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the
Official Toboggan Corporate Policy that was in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted
database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

Each line gives the password policy and then the password. The password
policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For
example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b,
but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits
of their respective policies.

How many passwords are valid according to their policies?

To begin, get your puzzle input.
"""
import input_


class Password:
    key = ''
    min_ = 1
    max_ = 1
    password = ''

    def __init__(self, line):
        self.min_, self.max_, self.key, self.password = self.parse_line(line)

    @staticmethod
    def parse_line(line: str):
        no_colon_line = line.replace(':', '')
        split_line = no_colon_line.split(' ')

        min_key_count, max_key_count = split_line[0].split('-')
        key = split_line[1]
        password = split_line[2]

        return int(min_key_count), int(max_key_count), str(key), str(password)


def valid_password(pw: Password):
    count = 0
    for k in pw.password:
        if k == pw.key:
            count += 1
    if count > pw.max_ or count < pw.min_:
        count = 0
    return True if count else False


def solve():
    file_ = input_.get_input_file(__file__)
    lines = input_.get_lines(file_)
    # lines = [
    #     '1-3 a: abcde',
    #     '1-3 b: cdefg',
    #     '2-9 c: ccccccccc',
    # ]

    valid_passwords = 0

    for l in lines:
        valid_passwords += 1 if valid_password(Password(l)) else 0

    return valid_passwords


if __name__ == '__main__':
    print(solve())
