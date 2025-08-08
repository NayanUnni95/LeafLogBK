from enum import Enum


class LoginField(Enum):
    NAME = 'name'
    EMAIL = 'email'
    PASSWORD = 'password'
    OTP = 'otp'

class FormUtil:

    @staticmethod
    def form_data_to_json(fields):
        datas = {}
        for field in fields:
            datas[field] = fields[field]
        return datas