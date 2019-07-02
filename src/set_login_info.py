#!/usr/bin/env python3
import sys
try:
    import keyring
except ModuleNotFoundError:
    print("keyring not found; install keyring via conda or pip.")
    sys.exit()

ATCODER_SERVICE = "atcoder-sample-test"


if __name__ == "__main__":
    print("Enter AtCoder username: ", end="")
    username = input()
    print("Enter AtCoder password: ", end="")
    password = input()
    keyring.set_password(ATCODER_SERVICE, ATCODER_SERVICE, username)
    keyring.set_password(ATCODER_SERVICE, username, password)
