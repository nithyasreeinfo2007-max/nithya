import json

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import (
    ComicRequest,
    OutlineResponse,
    StoryResponse,
)


def get_client():
    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    return genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_story(
    request: ComicRequest,
    outline: OutlineResponse,
) -> StoryResponse:

    client = get_client()

    outline_json = outline.model_dump_json(indent=2)

    prompt = f"""
Expand the following comic outline into a complete comic story.

User preferences:

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

Outline:
{outline_json}

Requirements:

- Return exactly one story object for every panel.
- Preserve panel numbers.
- Preserve story continuity.
- Keep the same main character.
- scene_description should be vivid but concise.
- caption should be a short comic caption.
- narration should describe action, emotion or context.
- dialogue should contain natural character dialogue.
- If no dialogue is needed, return an empty string.
- Keep the requested tone consistent.
"""

    response = client.models.generate_content(
        model=settings.GEMINI_STORY_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
            response_schema=StoryResponse,
        ),
    )

    if getattr(response, "parsed", None):
        if isinstance(response.parsed, StoryResponse):
            return response.parsed

    raw = getattr(response, "text", "") or ""

    try:
        return StoryResponse.model_validate(
            json.loads(raw)
        )
    except Exception as exc:
        raise RuntimeError(
            f"Gemini story returned invalid JSON: {raw[:500]}"
        ) from exc