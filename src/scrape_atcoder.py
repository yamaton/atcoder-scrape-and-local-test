#!/usr/bin/env python3
"""
Web-scrape input and output samples from a AtCoder problem, then returns the information in JSON

"""
import urllib.request
import argparse
import json
import sys
import itertools as it
import logging
import bs4  # BeautifulSoup 4


ATCODER_PROBLEM_URL = "https://atcoder.jp/contests/{}/tasks/{}"


def is_valid(prob_id):
    """
    Check if the given string is proper CodeForces problem ID.

    Args:
        prob_id (str): problem ID to be examined

    Return:
        bool.

    >>> is_proper('abc130_f')
    True

    >>> is_proper('dp_k')
    True

    >>> is_proper('abcde')
    False
    """
    if "_" not in prob_id:
        return False

    index = prob_id.split("_")[-1]
    if (len(index) != 1) or (not index.isalpha()):
        return False

    return True


def check_sanity(prob_id):
    """
    Exit if given string is NOT a CodeForces problem ID.

    Args:
        prob_id (str): problem ID to be examined

    Return:
        None
    """
    msg = "Problem ID {} has bad format!".format(prob_id)
    if not is_valid(prob_id):
        sys.exit(msg)


def geturi(prob_id, url=ATCODER_PROBLEM_URL):
    """
    Returns CodeForces URL for given problem ID.

    Args:
        prob_id (str)
        url (str)

    Returns:
        str

    >>> geturl("abc130_f")
    "https://atcoder.jp/contests/abc130/tasks/abc130_f"
    """
    tmp = prob_id.split("_")
    contest_id = "_".join(tmp[:-1])
    return url.format(contest_id, prob_id)


def save_samples(jsonstr):
    """
    Save input and output as text files from JSON string

    Args:
        jsonstr (str): JSON string with
            'sample_io_pairs' -> list of pair of (sample_input, sample_output)
            'id'

    input file is saved as '<problem_id>_<index>.in' like '23C_0.in'
    output file is saved as '<problem_id>_<index>.out' like '11A_1.out'
    """
    data = json.loads(jsonstr)
    problem_id = data["id"]
    sample_ios = data["sample_io_pairs"]

    for i, (inp, out) in enumerate(sample_ios):
        name = problem_id + "_" + str(i)
        with open(name + "_in.txt", "w") as f:
            for line in inp:
                print(line, file=f)
        with open(name + "_out.txt", "w") as f:
            for line in out:
                print(line, file=f)


def extract_samples(problem_str):
    """
    Go to CodeForces website and return input/output samples in JSON string

    Args:
        problem_str (str): proble ID

    Returns:
        str. JSON string of the form
        {
            'id': ...
            'url': ...
            'sample_io_pairs' : [ (input_lines, output_lines) ]
        }

    >>> extract_samples('abc130_a')
    {'id': 'abc130_a', 'url': 'https://atcoder.jp/contests/abc130/tasks/abc130_a', 'sample_io_pairs: [('3 5', '0'), ('7 5', '10'), ('6 6', '10')]}
    """
    check_sanity(problem_str)
    uri = geturi(problem_str, ATCODER_PROBLEM_URL)

    logging.info("Accessing: {}".format(uri))
    with urllib.request.urlopen(uri) as f:
        rawhtml = f.read()

    soup = bs4.BeautifulSoup(rawhtml, "html.parser")
    input_sample_anckers = [x for x in soup.find_all("h3") if "Sample Input" in x.text]
    inputs = [x.next.next.text.splitlines() for x in input_sample_anckers]
    output_sample_anckers = [x for x in soup.find_all("h3") if "Sample Output" in x.text]
    outputs = [x.next.next.text.splitlines() for x in output_sample_anckers]

    input_output_pairs = list(zip(inputs, outputs))
    result = {"id": problem_str, "url": uri, "sample_io_pairs": input_output_pairs}
    return json.dumps(result, indent=2)  # indent for pretty printing


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prob_id", help="Problem ID as in the AtCoder's URI (such as 'abc130_a')")
    args = parser.parse_args()
    s = args.prob_id
    jsonstr = extract_samples(s)
    print("[INFO] saving sample input and output as {}_*_in.txt and {}_*_out.txt".format(s, s))
    save_samples(jsonstr)
