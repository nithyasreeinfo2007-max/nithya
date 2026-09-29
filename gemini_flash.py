import json

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import ComicRequest, OutlineResponse


def get_client():
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    return genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_outline(request: ComicRequest) -> OutlineResponse:
    client = get_client()

    prompt = f"""
Create a cohesive {settings.NUM_PANELS}-panel comic outline.

Story prompt:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

- Exactly {settings.NUM_PANELS} panels.
- Maintain the same main character across all panels.
- Maintain visual continuity.
- Give every panel a clear title.
- Give every panel a concise scene description.
- Create a detailed image_prompt for every panel.
- Do not put dialogue inside image_prompt.
- Story must have a beginning, development, climax and ending.
"""

    response = client.models.generate_content(
        model=settings.GEMINI_OUTLINE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
            response_schema=OutlineResponse,
        ),
    )

    if getattr(response, "parsed", None):
        if isinstance(response.parsed, OutlineResponse):
            return response.parsed

    raw = getattr(response, "text", "") or ""

    try:
        return OutlineResponse.model_validate(
            json.loads(raw)
        )
    except Exception as exc:
        raise RuntimeError(
            f"Gemini outline returned invalid JSON: {raw[:500]}"
        ) from exc