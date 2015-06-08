from operator import itemgetter
import re


def split1space(s):
    spl = s.split(' ', 1)
    if len(spl) > 1:
        return [spl[0].strip(), spl[1].strip()]
    else:
        return ['', s]


def camelcase(s):
    s = s.strip()
    s = s.lower()
    s = re.sub('([a-z])[a-z]*', lambda x: x.group(1).upper() + x.group(0)[1:], s)
    return s


class Parser(object):
    def __init__(self, filename):
        self.filename = filename

        self.records = []

    def parse(self, ignore_headers=None, limit=None):
        with open(self.filename, 'r') as f:
            # not readlines() to be compatible with windows
            lines = f.read().splitlines()

        if limit is None:
            limit = -1
        if ignore_headers is None:
            ignore_headers = 0

        for line in lines[ignore_headers:limit]:
            self.records.append(line.split(','))

        print "Parsed %d records" % len(self.records)

    def dedupe(self, fields):
        print "Deduplicating on columns %s" % fields
        fields = fields.split(',')
        already_seen = {}
        processed = []
        duplicates = []
        for rec in self.records:
            h = ''.join([rec[int(x)] for x in fields])

            if h in already_seen:
                duplicates.append(rec)
            else:
                already_seen[h] = True
                processed.append(rec)

        self.records = processed
        if duplicates:
            dupe_filename = self.filename + '_dupes'
            print "Found %d duplicates, outputting them to %s" % (len(duplicates), dupe_filename)
            with open(dupe_filename, 'w') as f:
                for rec in duplicates:
                    f.write(','.join(rec) + '\n')
        else:
            print "No duplicates found"

    def ignore(self, ignore_exps=None):
        ignored_rows = []
        non_ignored_rows = []

        if not ignore_exps:
            return

        ignore = []
        for exp in ignore_exps:
            col, regex = exp.split(':')
            ignore.append((int(col), re.compile(regex)))

        for rec in self.records:
            for col, regex in ignore:
                if regex.search(rec[col]):
                    print "Ignoring record %r" % rec
                    ignored_rows.append(rec)
                else:
                    non_ignored_rows.append(rec)

        print "Ignored %d rows" % len(ignored_rows)
        self.records = non_ignored_rows

    def output(self, remapping=None, sort=None, output_headers=None):
        output_records = []

        remap = []
        if remapping:
            remapping = remapping.split(',')
            for x in remapping:
                try:
                    newcol = int(x)
                except ValueError:
                    # constant to fill the column with
                    newcol = x
                remap.append(newcol)


        for rec in self.records:
            rec_to_write = rec
            if remap:
                new_r = []
                for x in remap:
                    if isinstance(x, int):
                        new_r.append(rec[x])
                    else:
                        new_r.append(x)
                rec_to_write = new_r

            output_records.append(rec_to_write)

        if sort is not None:
            sort = int(sort)
            output_records.sort(key=itemgetter(sort))

        output_f = self.filename.replace('.csv', '_output.csv')
        if output_headers:
            outpnum = len(output_headers.split(','))

        with open(output_f, 'w') as f:
            if output_headers:
                if remap:
                    exp_len = len(remap)
                else:
                    exp_len = len(rec[0])
                assert exp_len == outpnum, "Headers must be the same size as destination %d/%d" % (exp_len, outpnum)
                f.write(output_headers + '\n')

            for rec in output_records:
                f.write(','.join(r.replace(',', '') for r in rec) + '\n')

        print "Output result to %s (records: %d)" % (output_f, len(output_records))

    def transform(self, transform_exps=None):
        transformed = []

        if not transform_exps:
            return

        transform = []
        for exp in transform_exps:
            col, modifier = exp.split(':')
            # FIXME ugly but...
            transform.append((int(col), globals()[modifier]))

        print "Printing 5 first transforms"
        for i, rec in enumerate(self.records):
            if i < 5:
                print "-----------\nBEFORE: %s" % rec
            new_r = rec
            for col, modif in transform:
                new = modif(new_r[col])
                if not isinstance(new, list):
                    new = [new]

                new_r = new_r[:col] + new + new_r[col+1:]

            if i < 5:
                print "AFTER: %s\n----------" % new_r
            transformed.append(new_r)

        self.records = transformed
