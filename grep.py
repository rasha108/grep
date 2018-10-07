import argparse
import sys
import re



import argparse
import sys
import re


def output(line):
    print(line)

def Index_difinition(pattern, lines, b_context, context, a_context):
    index = []
    new_index = []

    for idx, line in enumerate(lines):
        if pattern in line:
            index.append(idx)

    if b_context > 0:
        count = b_context
        for x in index:
            for j in range(count + 1):
                y = x - (count - j)
                if y >= 0 and not y in new_index:
                    new_index.append(y)

    if a_context > 0:
        count = a_context
        for x in index:
            for j in range(count + 1):
                y = x + j
                if y >=0 and y < len(lines) and not y in new_index:
                    new_index.append(y)

    if context > 0:
        count = context
        for x in index:
            for j in range(count + 1):
                y = x - (count - j)
                if y >= 0 and not y in new_index:
                    new_index.append(y)
            for j in range(count + 1):
                y = x + j
                if y >=0 and y < len(lines) and not y in new_index:
                    new_index.append(y)

    return new_index

def compare(pattern, line, case, invert):
    flag = re.IGNORECASE if case else 0
    match = re.search(pattern, line, flag)
    if invert:
        match = not match
    return match

def Context(idx, valid_index):
    if idx in valid_index:
        return 1
    return 0

def Search_pattern(pattern, line):
    search = re.search(pattern, line)
    print(search)
    if not search:
        return 0
    return 1

def grep(lines, params):
    a = 0
    params.pattern = params.pattern.replace('?', '.').replace('*','.*?')
    for n, line in enumerate(lines):
        line = line.rstrip()
        if params.ignore_case or params.invert:
            if params.count:
                if compare(params.pattern, line, params.ignore_case, params.invert) and params.line_number:
                    a += 1
                    output('{}:{}'.format(n, line))

                if compare(params.pattern, line, params.ignore_case, params.invert):
                    a += 1
                    output('{}'.format(line))

            else:
                if compare(params.pattern, line, params.ignore_case, params.invert):
                    if params.line_number:
                        output('{}:{}'.format(n, line))
                    else:
                        output(line)


        if not params.ignore_case and not params.invert and not params.count and not params.context and not params.before_context and not params.after_context:
            if params.line_number:
                if re.search(params.pattern, line):
                    output('{}:{}'.format(n, line))


        if not params.ignore_case and not params.invert and not params.line_number and not params.context and not params.before_context and not params.after_context:
            if params.count:
                if re.search(params.pattern,line):
                    a+=1

        if params.context or params.before_context or params.after_context:
            valid_index = Index_difinition(params.pattern, lines, params.before_context,
                                           params.context, params.after_context)
            if params.context:
                if Context(n, valid_index):
                    if params.line_number:
                        output('{}:{}'.format(n, line))
                    else:
                        output(line)
            if params.before_context:
                if Context(n, valid_index):
                    if params.line_number:
                        output('{}:{}'.format(n, line))
                    else:
                        output(line)
            if params.after_context:
                if Context(n, valid_index):
                    if params.line_number:
                        output('{}:{}'.format(n, line))
                    else:
                        output(line)

        elif not params.invert and not params.ignore_case and not params.count and not params.line_number \
                and not params.context and not params.before_context and not params.after_context:
            if Search_pattern(params.pattern, line):
                output(line)

    if params.count:
        output('{}'.format(a))


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
