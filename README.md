# Second lowest cost silver plan

## Coding

This is coded on python, using native libraries, so there's no need to install any libraries. This is coded in 
Python and can be run by inside this library with the following commands:

```
$ python slcsp.py

```

### Modularization
I've divided the script through the four stages by which the files are to be processed in order to get the desired outcome:

1. **`get_slcsp_per_rate_area`** : this goes through the `plans.csv` file once as well as takes the two lowest rates per rate area and updates it as we progress through the file. So we always keep the size of the arrays per ratee area to 2.

2. **`get_rate_area_zip`**: this processes the zipcode and pulls in the rate areas that aree within the zipcode. If a zipcode has two rate areas, it will be ambiguous for us to get the SLCSPs and thus will allow us to set the result to BLANK as per the task specifications.

3. **`get_slcsp`**: This process searches for the correct zipcode matching for a rate area and gets the second element, this pertains to the SLCSP requested for that zipcode.

4. **`write_results`**: This will write the results per zipcode into `slcsp_results.csv`


## Output

This will output a file called `slcsp_results.csv`. It would look more or less like `slcsp_results.csv.sample`. This will include the necessary outputs requested from the problem below.

## Testing

I did random manual testing to confirm the validity of the results.

# About the Task: Calculate the second lowest cost silver plan (SLCSP)

## Problem

You've been asked to determine the second lowest cost silver plan (SLCSP) for
a group of ZIP codes.

## Task

You've been given a CSV file, `slcsp.csv`, which contains the ZIP codes in the
first column. Fill in the second column with the rate (see below) of the
corresponding SLCSP and emit the answer as a CSV on stdout. Write your code in your best programming language.

### Expected output

The order of the rows in your answer as emitted on stdout must stay the same as how they
appeared in the original `slcsp.csv`. The first row should be the column headers: `zipcode,rate`
The remaining lines should output unquoted values with two digits after the decimal
place of the rates, for example: `64148,245.20`.

It may not be possible to determine a SLCSP for every ZIP code given; for example, if there is only one silver plan available, there is no _second_ lowest cost plan. Check for cases where a definitive answer cannot be found and leave those cells blank in the output CSV (no quotes or zeroes or other text). For example, `40813,`.

## Additional information

The SLCSP is the so-called "benchmark" health plan in a particular area. It's
used to compute the tax credit that qualifying individuals and families receive
on the marketplace. It's the second lowest rate for a silver plan in the rate area.

For example, if a rate area had silver plans with rates of `[197.3, 197.3, 201.1, 305.4, 306.7, 411.24]`, the SLCSP for that rate area would be `201.1`,
since it's the second lowest rate in that rate area.

A plan has a "metal level", which can be either Bronze, Silver, Gold, Platinum,
or Catastrophic. The metal level is indicative of the level of coverage the plan
provides.

A plan has a "rate", which is the amount that a consumer pays as a monthly
premium, in dollars.

A plan has a "rate area", which is a geographic region in a state that
determines the plan's rate. A rate area is a tuple of a state and a number, for
example, NY 1, IL 14.

There are two additional CSV files in this directory besides `slcsp.csv`:

- `plans.csv` — all the health plans in the U.S. on the marketplace
- `zips.csv` — a mapping of ZIP code to county/counties & rate area(s)

A ZIP code can potentially be in more than one county. If the county can not be
determined definitively by the ZIP code, it may still be possible to determine
the rate area for that ZIP code. A ZIP code can also be in more than one rate area. In that case, the answer is ambiguous
and should be left blank.

We will want to compile your code from source and run it, so please include the
complete instructions for doing so in a COMMENTS file.
