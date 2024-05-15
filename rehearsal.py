def check_authorization(auth_code: int, nth_switch: int):
    return auth_code & (1 << nth_switch) != 0

if __name__ == "__main__":
    print(check_authorization(21, 0))
