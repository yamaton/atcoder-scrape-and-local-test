# AtCoder Sample Cases Tester

Run your answer to AtCoder problems with sample cases **without copy-pasting**! This script scrapes sample inputs/outputs, and then run your code with the sample cases. It can handle Python, C++, Haskell.

## Requirement

-   Python 3.x
-   [Beautiful Soup 4](<http://www.crummy.com/software/BeautifulSoup/>)


## Usage

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash
atcoder <path/to/your/solution.cpp>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**NOTE:** the filename or file path **must** contain a problem ID. You may have another
string in the filename as long as they are separated by space ` `, or hyphen
`-`, or underscore `_`. For example, following filenames are all allowed.

* abc130_a.cpp
* abc130/a.py
* abc130/a-Rounding.rs



The script `run_with_atcoder_sample.py` feeds the samples cases to your code as standard input, and returns “ok” if the standard output agrees with the samples.



[FILL OUT SAMPLE SCREENSHOT -- SUCCESS]



Otherwise, it returns “Incorrect”, and shows sample input, your output, and sample output. This happens as long as output strings do not agree **exactly**.



[FILL OUT SAMPLE SCREENSHOT -- FAILURE]





## Configuration

Compilation options follows the [official rules](https://atcoder.jp/contests/agc034/rules). For example

**C++:**

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~bash
g++ -std=gnu++1y -o <your-code>.exe <your-code>.cc
<your-code>.exe < <scraped-sample-input>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

