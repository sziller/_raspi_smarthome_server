from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_psswd_hash(psswd):
    return pwd_context.hash(psswd)


if __name__ == "__main__":
    psswd = "guest"
    print(psswd)
    print(get_psswd_hash(psswd=psswd))
    
