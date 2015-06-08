from argparse import ArgumentParser
import sys

from csvmanipulator.parser import Parser


def main():
    parser = ArgumentParser()
    parser.set_defaults(func=run)
    parser.add_argument('--ignore-headers', type=int, help='remove the N first lines of the file')
    parser.add_argument('--limit', type=int, help='limit parsing to the first N lines of the file')
    parser.add_argument('--dedupe', help='dedupe on column X,Y (first: 0)')
    parser.add_argument('--remapping', help='remap column in the final csv: 3,4,0,1')
    parser.add_argument('--sort', help='sort the final csv by the column X, POST-remapping')
    parser.add_argument('--ignore', action='append', help='should be col:regex to ignore certain records')
    parser.add_argument('--modifier', action='append', help='should be col:<modifier> where modifier is split1space,camelcase')
    parser.add_argument('--output-headers', help='add these headers to the output')
    parser.add_argument('filename', help='input file path')

    options = parser.parse_args()
    sys.exit(options.func(options))


def run(options):
    p = Parser(options.filename)
    p.parse(ignore_headers=options.ignore_headers, limit=options.limit)

    if options.modifier:
        p.transform(transform_exps=options.modifier)

    if options.dedupe is not None:
        p.dedupe(options.dedupe)

    if options.ignore:
        p.ignore(ignore_exps=options.ignore)

    p.output(remapping=options.remapping, sort=options.sort, output_headers=options.output_headers)
