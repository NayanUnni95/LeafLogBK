from enum import Enum

class Roles(str, Enum):
    ADMIN = "Admin"
    OWNER = "Owner"
    USER = "User"

    HIERARCHY = {
        "Admin": 1,
        "Owner": 2,
        "User": 3
    }

    @staticmethod
    def get_all_role_types():
        return [role.value for role in Roles]
    
    @staticmethod
    def from_string(role_str):
        for role in Roles:
            if role.value == role_str:
                return role
        
        return None
    
    @classmethod
    def admin_access(cls) -> list[str]:
        return [cls.ADMIN.value, cls.OWNER.value]
    
    @classmethod
    def user_access(cls) -> list[str]:
        return [cls.ADMIN.value, cls.OWNER.value, cls.USER.value]
    

class JWTTokenKey(Enum):
    ID = 'id'
    EXPIRY = 'expiry'
    TOKEN_TYPE = 'token_type'
    IS_GUEST = 'is_guest'
    LOGIN_ATTEMPT_ID = 'login_attempt_id'
    PRODUCT_NAME = 'product_name'


class Algorithm(Enum):
    HS256 = 'HS256'