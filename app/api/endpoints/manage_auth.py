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


@router.post('/login/')
async def login(request: Request, db: SessionDep):
    try:
        data = FormUtil.form_data_to_json(await request.form())
    except MultipartParseError:
        data = {}
    email = data.get('email')

    if not (user := (await db.scalar(select(User).filter(User.email == email)))):
        if not (name := data.get('name')):
            return CustomResponse(general_message="name field is required.").get_failure_response()

        if not (password := data.get('password')):
            return CustomResponse(message="password field is required.").get_failure_response()

        user = User(
            name=name,
            email=email,
            password=Hash.encrypt_password(password) if password else None,
            role=Roles.USER.value
        )
        # user_id = user.id
        # user_email = user.email
        # user_name = user.name
        # user_role = user.role
        # user_access_token = JWTUtil.create_access_token({"id": user_id})
        # user_refresh_token = JWTUtil.create_refresh_token({"id": user_id})

    # to_email = user.email
    # otp = Hash.generate_otp()
    # subject = f'{otp} - Login otp'
    # message = f'OTP {otp} - for login leaflog dashboard.'
    # try:
    #     user.otp = int(otp)
    #     await MailUtil.email_without_attachment(to_email, subject, message)
    # except Exception as e:
    #     print(e)

    db.add(user)
    await db.commit()
    return CustomResponse(
        general_message="User successfully onboard."
    ).get_success_response()


@router.post('/verify-user/')
async def get_otp(request: Request, db: SessionDep):
    try:
        data = FormUtil.form_data_to_json(await request.form())
    except MultipartParseError:
        data = {}

    email = data.get('email') or None
    password = data.get('password') or None

    if not email:
        return CustomResponse(general_message="OTP field is required.").get_failure_response()

    if not password:
        return CustomResponse(general_message="password field is required.").get_failure_response()

    if not (user := (await db.scalar(select(User).filter(User.email == data.get('email'))))):
        return CustomResponse(general_message="User not found.").get_failure_response()
    
    if password and not Hash.verify_password(password, user.password):
        return CustomResponse(general_message="Invalid password.").get_failure_response()
    

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