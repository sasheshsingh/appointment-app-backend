from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(self, password):
        return pwd_context.hash(password)

    def verify_password(self, password, hash):
        return pwd_context.verify(password, hash)
