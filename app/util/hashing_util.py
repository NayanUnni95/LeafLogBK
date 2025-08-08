import random
import string

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash:

    @staticmethod
    def encrypt_password(password: str):
        return pwd_context.hash(password)


    @staticmethod
    def verify_password(password: str, hashed_password: str):
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def generate_otp(length = 6):
        if not isinstance(length, int) or length <= 0:
            raise ValueError("OTP length must be a positive integer.")

        otp = ''.join(random.choice(string.digits) for _ in range(length))
        return otp