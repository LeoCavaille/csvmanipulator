Manipulate CSVs and transform them in other CSVs
-------------------------------------------------

Just install the package and run `csvmanip <options> <csv_file_input>` where the options configure the steps below.

The only limitation is that your input CSV file must only contain `,` as delimiters (no commas inside columns escaped or anything).

### Step 1: Parsing

Parses your CSV file.

* `--ignore_headers N`, ignores N lines at the beginning (typically the headers and padding of input file)
* `--limit N`, only parse the first N lines of the input

### Step 2: Normalization

Allows you to plug modifiers, to make the input look prettier. Right now only two modifiers exist:

* `split1space` transforms a column in 2 columns by splitting at the first name (e.g. use it for "Name Surname")
* 'camelcase` transforms a string BLA in Bla

Use as many `--modifier colnum:function` as you wish. Be careful if you transform a column into more now columns, each modifier is run sequentially therefore the colnum should be changed accordingly.

### Step 3: Deduplication

Deduplicate records by using one or more column as unique key. Use `--dedupe` with a number or comma-separated list of numbers.

### Step 4: Ignoring records

If you want to ignore records, pass in one or multiple `--ignore colnum:regex` expressions. Self-explanatory.

### Step 5: Outputting a new CSV

By default it will output the current set of records, if you want to change the columns, use `--remapping` and pass in a list of integers or strings:

* an integer represents a column in the current set of records
* a string will be replace as is at that position in the new records

You can also use `--output-headers` if you want to add a custom description in the first line of all the new records (comma-separated list of strings)

Eventually sort the records by using `--sort colnum` where colnum represents the column index in the NEW records to be output.
