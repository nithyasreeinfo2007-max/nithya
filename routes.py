from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .schemas import ComicRequest, ComicResponse
from .image_generator import generate_image


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@router.post(
    "/api/generate",
    response_model=ComicResponse
)
async def generate_comic(data: ComicRequest):

    panels = []

    for i in range(1, data.num_panels + 1):

        image_prompt = (
            f"{data.art_style} comic panel, "
            f"{data.prompt}, "
            f"panel {i}, "
            "professional comic illustration, "
            "clear characters, detailed background, "
            "cinematic lighting, no text, no watermark"
        )

        image_url = None

        try:
            image_url = generate_image(
                prompt=image_prompt,
                panel_number=i
            )

        except Exception as e:
            print(
                f"Image generation failed for panel {i}: "
                f"{type(e).__name__}: {e!r}"
            )

        panel = {
            "panel_number": i,
            "narration": (
                f"Panel {i}: {data.prompt}"
            ),
            "dialogue": [],
            "image_prompt": image_prompt,
            "image_url": image_url
        }

        panels.append(panel)

    return {
        "title": "ComicCraft AI Comic",
        "panels": panels
    }