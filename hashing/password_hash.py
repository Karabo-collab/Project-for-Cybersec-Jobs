import bcrypt



def password_hasher(password):
    """
    This function accepts a password string,
    encodes it into bytes,
    generates a random salt,
    and returns the bcrypt hash.
    """

    encoded_password = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        encoded_password,
        salt
    )

    return hashed_password


user_password = input("Enter a password: ")

hashed_password = password_hasher(user_password)

print(f"Original Password: {user_password}")
print(f"Hashed Password: {hashed_password.decode()}")
