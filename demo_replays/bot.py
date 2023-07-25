import requests
from autoblocks.tracer import AutoblocksTracer

from demo_replays.settings import env

PROVIDER = "openai"
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0
PROMPT = (
    "You will be provided with a text, and your task is to extract the airport codes from it. "
    "Return ONLY the airport codes."
)


def get_response(autoblocks: AutoblocksTracer, query: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        "temperature": TEMPERATURE,
    }

    req = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=payload,
        headers={"Authorization": f"Bearer {env.OPENAI_API_KEY}"},
        timeout=10,
    )
    req.raise_for_status()
    response = req.json()

    autoblocks.send_event(
        "chat.completion",
        properties=dict(
            provider=PROVIDER,
            payload=payload,
            response=response,
        ),
    )

    return response["choices"][0]["message"]["content"]
