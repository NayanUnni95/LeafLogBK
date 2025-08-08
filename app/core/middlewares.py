import io

import httpx
from  decouple import config as decouple_conf


async def send_log_to_discord(error_message: str, payload) -> None:
    if WEBHOOK_URL := decouple_conf("DISCORD_WEBHOOK_URL", default=None):
        message = f"Unhandled exception: {error_message} Additional Information: {payload}"
        log_file = io.StringIO()
        log_file.write(message)
        log_file.seek(0)

        file_data = {'file': ('log.txt', log_file.getvalue(), 'text/plain')}

        async with httpx.AsyncClient() as client:
            await client.post(WEBHOOK_URL, files=file_data)
        log_file.close()


async def send_discord_webhook(*messages) -> None:
    mm = []
    for message in messages:
        if isinstance(message, list):
            mm.extend(str(item) for item in message)
        if isinstance(message, dict):
            mm.extend(str(message))
        else:
            mm.append(str(message))

    if WEBHOOK_URL := decouple_conf("DISCORD_WEBHOOK_URL", default=None):
        async with httpx.AsyncClient(timeout=30.0) as client:
            await client.post(WEBHOOK_URL, json={'content': " ".join(mm)})