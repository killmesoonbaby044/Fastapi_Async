from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashing(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# def model_to_dict(model_obj):
#     result = model_obj.__dict__
#     result.pop('_sa_instance_state', None)
#     return result
