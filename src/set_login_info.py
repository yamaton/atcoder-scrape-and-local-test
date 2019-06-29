import keyring

ATCODER_SERVICE = "atcoder-sample-test"


if __name__ == "__main__":
    print("Enter AtCoder username: ", end="")
    username = input()
    print("Enter AtCoder password: ", end="")
    password = input()
    keyring.set_password(ATCODER_SERVICE, ATCODER_SERVICE, username)
    keyring.set_password(ATCODER_SERVICE, username, password)
