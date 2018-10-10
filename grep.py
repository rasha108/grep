import argparse
import sys
import re


def output(line):
    print(line)


def compare(pattern, line, case, invert):
    flag = re.IGNORECASE if case else 0
    match = bool(re.search(pattern, line, flag))
    if invert:
        match = not match
    return match


def count(lines, params):
    a = 0
    for line in lines:
        line = line.rstrip()
        if compare(params.pattern, line, params.ignore_case, params.invert):
            a += 1
    output('{}'.format(a))


def grep(lines, params):
    params.pattern = params.pattern.replace('?', '.').replace('*', '.*?')


    before = max(params.context, params.before_context)
    after = max(params.context, params.after_context)

    if params.count:
        count(lines, params)

    else:
        count_after = 0
        buffer = [None] * before

        for n, line in enumerate(lines):
            line = line.rstrip()

            if compare(params.pattern, line, params.ignore_case, params.invert):
                if buffer:
                    print(buffer)
                    for id_bf, line_bf in enumerate(buffer):
                        if line_bf:
                            if params.line_number:
                                line_bf = '{}-{}'.format(n - before + id_bf + 1, line_bf)
                            output(line_bf)

                    buffer = [None] * before

                if params.line_number:
                    line = '{}:{}'.format(n + 1, line)
                output(line)

                count_after = after

            elif count_after:
                count_after -= 1
                if params.line_number:
                    line = '{}-{}'.format(n + 1, line)
                output(line)

            else:
                buffer.append(line)
                if len(buffer) > before:
                    buffer.pop(0)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
