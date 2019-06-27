#!/usr/bin/env python3
"""
Codeforces Automatic Testing with Sample Input/Output

@author yamaton
@date 2015-08-31
      2015-09-27
      2015-11-20  Test C++, Haskell, and Scala in addition to Python
      2015-12-06  Moved to GitHub repository
      2018-11-27  Applied black. Adapt to new input/output
"""
import argparse
import subprocess
import sys
import os
import pathlib
import json
import logging
import re
import inspect

pp = os.path.abspath(os.path.dirname(inspect.getsourcefile(lambda: 0)))
sys.path.append(pp)

from scrape_atcoder import extract_samples, is_valid


class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def bold(s):
    return colors.BOLD + s + colors.ENDC


def blue(s):
    return colors.OKBLUE + s + colors.ENDC


def green(s):
    return colors.OKGREEN + s + colors.ENDC


def red(s):
    return colors.FAIL + s + colors.ENDC


def orange(s):
    return colors.WARNING + s + colors.ENDC


def extract_id(filepath):
    """
    Extract Codeforces problem ID in filename string.

    Args:
        filepath (pathlib.Path or str)
    Returns:
        str or None

    >>> extract_id('abc130/a.cc')
    'abc130_a'

    >>> extract_id('abc130_a.py')
    'abc130_a'

    >>> extract_id('ABC130a.cc')

    >>> extract_id('abc130-a-comment.cc')
    'abc130_a'
    
    >>> extract_id('abc130_a Rounding.py')
    'abc130_a'

    >>> extract_id('abc130_a_Rounding.py')
    'abc130_a'

    >>> extract_id('ABC130/A-Rounding.py')
    'abc130_a'

    >>> extract_id('abc130/aRounding.py')

    >>> extract_id('abc130/123_baz.py')

    >>> extract_id('arc012/abc099_a.py')
    'abc099_a'
    """
    p = pathlib.Path(filepath).absolute()
    filename_stem = p.stem.lower()
    logging.debug("filename_stem = {}".format(filename_stem))

    groups = re.split(r"[ _-]", filename_stem)
    candidate = "_".join(groups[:2])

    if not is_valid(candidate):
        # if filename alone cannot resolve the ID
        # use parent directory's name as well
        candidate = None
        prefix = groups[0]
        if len(prefix) == 1 and prefix.isalpha():
            parent_dir = p.parent.name.lower()
            tmp = parent_dir + "_" + prefix
            if is_valid(tmp):
                candidate = tmp
    
    return candidate


def run_code(filepath, inp):
    """
    Run C++/Python/Haskell code against given inp

    Args:
        filepath (pathlib.Path): filename of python code
        inp (list of str): sample input
    """
    filepath = filepath.absolute()
    p_src = filepath.as_posix()
    base, ext = filepath.stem, filepath.suffix
    exe_ext = ".exe"
    p_exe = (filepath.parent / (base + exe_ext)).as_posix()

    # C++
    if ext in (".cc", ".cp", ".cpp", ".c++", ".cxx"):
        subprocess.run(["g++", "-std=gnu++1y", "-O2", "-o", p_exe, p_src])
        com = [p_exe]
    # Python
    elif ext == ".py":
        com = [sys.executable, p_src]
    # Rust
    elif ext == ".rs":
        subprocess.run(["rustc", "-O", "-o", p_exe, p_src])
        com = [p_exe]
    # F#
    elif ext in (".fs", ".fsx"):
        subprocess.run(["fsharpc", p_src])
        com = ["mono", p_exe]
    # Haskell
    elif ext == ".hs":
        subprocess.run(["ghc", "-O2", "-Wall", p_src, "-o", p_exe])
        com = [p_exe]
    # Kotlin
    elif ext == ".kt":
        p_jar = filepath.parent / (base + ".jar")
        classname = filepath.stem.capitalize() + "Kt"
        subprocess.run(["kotlinc", p_src, "-include-runtime", "-d", p_jar])
        com = ["kotlin", "-classpath", p_jar, "-J-Xss256M", classname]
    # Nim
    elif ext == ".nim":
        subprocess.run(["nim", "c", "-d:release", "-o:" + p_exe, p_src])
        com = [p_exe]
    else:
        sys.exit("I can take only .py, .cc, .fs, .hs, .kt")

    p_src = subprocess.Popen(com, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = p_src.communicate(inp.encode())  # encode: string -> bytestring
    out = out.decode().strip()  # decode: bytestring -> string
    return out


def compare(inputs, outputs, groundtruth):
    """
    inputs   [str]
    outputs  [str]
    groundtruth [str]
    """
    assert len(inputs) == len(outputs) == len(groundtruth), "Mismatching size!"

    for i, (inp, user_out, samp_out) in enumerate(zip(inputs, outputs, groundtruth)):
        print(blue("Case {}".format(i + 1)) + ": ", end="")
        samp_out = samp_out.strip()
        user_out = user_out.strip()
        if samp_out == user_out:
            print(green("ok"))
        else:
            print(red("============ Mismatch ============"))
            print("Sample Input : ", inp)
            print("Sample Output: ", samp_out)
            print("Your Answer  : ", orange(user_out))


def main():
    """
    1. Get filename of Python code and problem ID
    2. Go to the CodeForces website and get input and output samples in JSON
    3. Get input/ouput string from JSON
    4. Run Python code with the sample input, and compare its outcome with the
    sample output.
    """
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input source code path")
    parser.add_argument("--contest", help="Weather it's AtCoder contest", default="yes")
    args = parser.parse_args()

    p = pathlib.Path(args.input)
    first_char = args.contest.lower()[0]
    if_login = first_char == "y" or first_char == "t"
    logging.debug("if_login: {}".format(if_login))

    assert p.exists(), "File not found: {}".format(args.input)
    filename = p.name
    problem_id = extract_id(p)
    assert problem_id, "Failed to deduce problem ID"
    print("\nAtCoder {}: {}".format(bold(problem_id), bold(filename)))

    json_str = extract_samples(problem_id, if_login)
    json_dict = json.loads(json_str)

    assert problem_id == json_dict["id"]
    sample_io_pairs = json_dict["sample_io_pairs"]

    inputs = ["\n".join(input_line_list) for (input_line_list, _) in sample_io_pairs]
    groupndtruths = [
        "\n".join(output_line_list) for (_, output_line_list) in sample_io_pairs
    ]
    outputs = [run_code(p, inp) for inp in inputs]
    compare(inputs, outputs, groupndtruths)


if __name__ == "__main__":
    main()
