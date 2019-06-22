import keyring

ATCODER_SERVICE = "atcoder-sample-test"


if __name__ == "__main__":
    print("Enter AtCoder username: ", end="")
    username = input()
    print("Enter AtCoder password: ", end="")
    password = input()
    keyring.set_password(ATCODER_SERVICE, username, ATCODER_SERVICE)
    keyring.set_password(ATCODER_SERVICE, username, password)
