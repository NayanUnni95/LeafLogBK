from datetime import datetime, date
from typing import Union

import pytz
from fastapi import Request
from starlette.websockets import WebSocket


class DateUtil:
    DATE_FORMATTED1 = "%d-%b-%Y"
    DATE_TIME_FORMATTED1 = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def to_datetime(date_time: str | None, date_only=False) -> datetime | None:
        """
        Converts a date-time string into a datetime object based on a specified format.

        Args:
            date_time: Date-time string to convert.
            date_only: If True, converts to a date object instead of a datetime object

        Returns:
            datetime: Parsed datetime object.
        """

        if not date_time:
            return None

        format_ = "%Y-%m-%d" if date_only else "%Y-%m-%d %H:%M:%S%z"
        try:
            return datetime.strptime(date_time, format_).date() if date_only else datetime.strptime(date_time, format_)
        except ValueError:
            format_ = "%Y-%m-%d %H:%M:%S"
            return datetime.strptime(date_time, format_).date() if date_only else datetime.strptime(date_time, format_)

    @staticmethod
    def get_current_time(timezone: Union[pytz.timezone, str] = None, date_only=False) -> datetime:
        """
        Retrieves the current time in the specified timezone, defaults to UTC if no timezone is provided.
        Can return just the date portion if date_only is set to True.

        Args:
            timezone: The timezone as a timezone object or a string that pytz can interpret.
            date_only: If True, returns just the date portion.

        Returns:
            datetime: Current time in the given timezone, with microseconds set to 0. If date_only is True, returns just
             the date.
        """
        if not timezone:
            timezone = pytz.timezone("UTC")
        elif isinstance(timezone, str):
            timezone = pytz.timezone(timezone)
        current_time = datetime.now(timezone).replace(microsecond=0)
        return current_time.date() if date_only else current_time

    @staticmethod
    def get_user_timezone(request: Union[Request, WebSocket], default_utc: bool = True) -> pytz.timezone:
        """
        Retrieves the user's timezone from a Request or WebSocket object's headers or query parameters.
        If the timezone is not provided or is invalid, it defaults to UTC or None based on the default_utc parameter.

        Args:
            request: The Request or WebSocket object to extract the timezone from.
            default_utc: If True, defaults to UTC timezone when no valid timezone is found, otherwise returns None.

        Returns:
            pytz.timezone: The timezone object corresponding to the user's timezone, or the default.
        """
        user_timezone_str = request.headers.get('timezone') if isinstance(request,
                                                                          Request) else request.query_params.get(
            "timezone")
        try:
            return pytz.timezone(user_timezone_str) if user_timezone_str else (
                pytz.timezone('UTC') if default_utc else None)
        except pytz.UnknownTimeZoneError:
            return pytz.timezone('UTC') if default_utc else None

    @staticmethod
    def formatted_datetime(date_time: Union[datetime, date], output_format) -> str:
        """
        Converts a timestamp string from one format to another.
        Args:
            date_time: Input timestamp string.
            output_format: Output format of the timestamp string.

        Returns:
            str: Formatted timestamp string.
        """
        return date_time.strftime(output_format)

    @staticmethod
    def convert_to_timezone(date_time: Union[datetime, str], timezone: Union[pytz.timezone, str]) \
            -> Union[datetime, None]:
        """
        Converts a datetime object or string to a datetime object in a specified timezone.

        Args:
            date_time: datetime object or string representing the date and time.
            timezone: Timezone to convert the datetime to, as either a pytz. Timezone object or a timezone string.

        Returns:
            datetime: Converted datetime object in the specified timezone.
        """
        if not date_time:
            return None
        if isinstance(date_time, str):
            date_time = DateUtil.to_datetime(date_time)
        if isinstance(timezone, str):
            timezone = pytz.timezone(timezone)
        return date_time.astimezone(timezone)

    @staticmethod
    def to_user_timezone(date_time: datetime, request: Union[Request, WebSocket] = None,
                         timezone: pytz.timezone = None) -> Union[str, None]:
        """
        Format a datetime object to a string in the user's timezone.
        Args:
            request: Request object containing headers.
            date_time: datetime object to format.

        Returns:
            str: Formatted datetime string in the user's timezone.
        """
        if not date_time:
            return None
        if not timezone and request:
            timezone = DateUtil.get_user_timezone(request)
        return DateUtil.convert_to_timezone(date_time, timezone).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def from_user_to_utc(date_time: str | None, request: Union[Request, WebSocket] = None,
                         timezone: pytz.timezone = None) -> datetime | None:
        """
        Converts a datetime string from the user's local timezone (obtained from the request) to UTC.

        Args:
            date_time: datetime string in the user's local timezone.
            request: Request or WebSocket object to extract the user's timezone from.
            timezone: Timezone to convert the datetime to, as either a pytz. Timezone object or a timezone string.

        Returns:
            datetime: The datetime object converted to UTC.
        """
        if date_time is None:
            return None

        if not timezone:
            timezone = DateUtil.get_user_timezone(request)

        if isinstance(timezone, str):
            timezone = pytz.timezone(timezone)

        local_date_time = timezone.localize(
            datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S'))
        return local_date_time.astimezone(pytz.utc)