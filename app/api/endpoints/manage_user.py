import requests
import json
import re

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


@router.post('/generate-task/')
async def generate_task(db: SessionDep, user: CurrentUserDep):
    user_id = user.get('id')

    # Check if user exists
    if not (user := (await db.scalar(select(User).filter(User.id == user_id)))):
        return CustomResponse(general_message="User not found.").get_failure_response()

    GEMINI_API_KEY = "AIzaSyB6jb3LQR2oF8s39MWuw_hypNdUP8DepLc"
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    current_week_tasks = [
    "Use reusable water bottle",
    "Switch off lights when not in use",
    "Plant a tree",
    "Recycle plastic bottles",
    "Avoid single-use plastics"
    ]

    prompt = f"""
    You are an eco-awareness and sustainability assistant for a premium website called "Leaflog".
    Your job is to generate the daily eco-awareness plan.

    Requirements:
        - You will be given a list of eco tasks already generated this week:
        {current_week_tasks}
        - Generate exactly 5 **new unique eco tasks** that are **NOT** in the list above.
        - For each task:
        - Give a short, clear, user-friendly description.
        - Assign **EcoCoins** for completion (between 5 and 50).
        - Provide measurable **impact** in one of the two formats:
            1. "CO₂ saved: X kg"
            2. "Water saved: X liters"
        - Add a **daily eco-friendly inspiration quote** (short, motivational).
        - Output must be **valid JSON** in the following exact structure:
    {{
        "tasks": [
            {{
                "task": "string",
                "eco_coins": integer,
                "impact": "string"
            }}
        ],
        "quote": "string"
    }}

    Strict Output Rules:
    1. Return ONLY the JSON object.
    2. Do NOT add ```json, backticks, or any code fences.
    3. Do NOT add explanations, notes, or extra text.
    4. The first character of your response must be '{{' and the last character must be '}}'.
    """


    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    # Call Gemini API
    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code != 200:
        return CustomResponse(
            general_message="Gemini API error",
            response=response.text
        ).get_failure_response()

    gemini_output = response.json()

    try:
        # Extract text output from Gemini
        generated_text = gemini_output["candidates"][0]["content"]["parts"][0]["text"]

        generated_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", generated_text.strip(), flags=re.MULTILINE)
        # Parse JSON directly
        parsed_output = json.loads(generated_text)
        print(parsed_output)

        # Validate structure
        if not isinstance(parsed_output.get("tasks"), list) or not isinstance(parsed_output.get("quote"), str):
            return CustomResponse(
                general_message="Gemini returned unexpected structure",
                response=parsed_output
            ).get_failure_response()

        return CustomResponse(response=parsed_output).get_success_response()

    except json.JSONDecodeError:
        return CustomResponse(
            general_message="Gemini returned invalid JSON",
            response=generated_text
        ).get_failure_response()
    except Exception as e:
        return CustomResponse(
            general_message="Error parsing Gemini response",
            response=str(e)
        ).get_failure_response()