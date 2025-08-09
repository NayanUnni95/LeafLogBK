from fastapi import APIRouter, Request
from multipart.exceptions import MultipartParseError
from sqlalchemy.sql import select

from app.api.deps import SessionDep, CurrentUserDep
from app.core.exception_handler import ExceptionLoggingRoute
from app.db.models import User
from app.util.form_util import FormUtil
from app.util.hashing_util import Hash
from app.util.jwt_util import JWTUtil
from app.util.communication_util import MailUtil
from app.util.types import Roles
from app.util.response import CustomResponse
from app.core.config import settings

router = APIRouter(route_class=ExceptionLoggingRoute)


# @router.post('/register/')
# async def register(request: Request, db: SessionDep):
    # try:
    #     data = FormUtil.form_data_to_json(await request.form())
    # except MultipartParseError:
    #     data = {}
    # email = data.get('email')
    # password = data.get('password')

    # if (await db.scalar(select(User).filter(User.email == email))):
    #     return CustomResponse(general_message="Email already exist.").get_failure_response()

    # user = User(name=email.split('@')[0], email=email, password=Hash.encrypt_password(password) if password else None,  role=Roles.VIEWER.value)
    # user_id = user.id
    # user_email = user.email
    # user_name = user.name
    # user_role = user.role
    # db.add(user)
    # await db.commit()
    # return CustomResponse(
    #     general_message="User successfully registered.",
    #     response={
    #         "id": user_id,
    #         "name": user_name,
    #         "email": user_email,
    #         "role": user_role
    # }).get_success_response()


@router.post('/login/')
async def login(request: Request, db: SessionDep):
    try:
        data = FormUtil.form_data_to_json(await request.form())
    except MultipartParseError:
        data = {}
    email = data.get('email')
    password = data.get('password')
    # otp = data.get('otp')

    if not (user := (await db.scalar(select(User).filter(User.email == email)))):
        if not (name := data.get('name')):
            return CustomResponse(message="name field is required.").get_failure_response()

        if not (password := data.get('password')):
            return CustomResponse(message="password field is required.").get_failure_response()

        user = User(name=name, email=email, password=Hash.encrypt_password(password) if password else None,  role=Roles.USER.value)
        user_id = user.id
        user_email = user.email
        user_name = user.name
        user_role = user.role
        user_access_token = JWTUtil.create_access_token({"id": user_id})
        user_refresh_token = JWTUtil.create_refresh_token({"id": user_id})

        db.add(user)
        await db.commit()
        return CustomResponse(
        general_message="User successfully registered.",
        response={
            "id": user_id,
            "name": user_name,
            "email": user_email,
            "role": user_role,
            "access_token_expiry": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "access_token": user_access_token,
            "refresh_token_expiry": settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            "refresh_token": user_refresh_token
        }).get_success_response()
    
    if password and not Hash.verify_password(password, user.password):
        return CustomResponse(general_message="Invalid password.").get_failure_response()

    # if not otp:
    #     return CustomResponse(message={"otp": "otp field is required."}).get_failure_response()

    # if otp != str(user.otp):
        # return CustomResponse(general_message="Invalid OTP!").get_failure_response()

    user_access_token = JWTUtil.create_access_token({"id": user.id})
    user_refresh_token = JWTUtil.create_refresh_token({"id": user.id})
    return CustomResponse(
        general_message="User login success.",
        response={
            "access_token_expiry": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "access_token": user_access_token,
            "refresh_token_expiry": settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            "refresh_token": user_refresh_token
    }).get_success_response()


# @router.get('/get-access-token/')
# async def get_access_token(db: SessionDep, current_user: CurrentUserDep):
    user_id = current_user.get('id')
    if not (user :=  (await db.scalar(select(User).filter(User.id == user_id)))):
        return CustomResponse(general_message="User not found.").get_failure_response()

    user_access_token = JWTUtil.create_access_token({"id": user_id})
    return CustomResponse(response={
        "expiry": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "token": user_access_token,
    }).get_success_response()


# @router.post('/generate-otp/')
# async def get_otp(request: Request, db: SessionDep):
#     try:
#         data = FormUtil.form_data_to_json(await request.form())
#     except MultipartParseError:
#         data = {}

#     if not (user := (await db.scalar(select(User).filter(User.email == data.get('email'))))):
#         return CustomResponse(general_message="User not found.").get_failure_response()

#     to_email = user.email
#     otp = Hash.generate_otp()
#     subject = f'{otp} - Login otp'
#     message = f'OTP {otp} - for login cemofficial dashboard.'
#     try:
#         user.otp = int(otp)
#         await MailUtil.email_without_attachment(to_email, subject, message)
#     except Exception as e:
#         print(e)

#     await db.commit()
#     return CustomResponse(general_message="Your OTP is sent to your email!",).get_success_response()