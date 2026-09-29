from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.image_generator import generate_image


app = FastAPI(title="ComicCraft")


# Static files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory="app/templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story: str = Form(...),
    character: str = Form(...),
    setting: str = Form(""),
    tone: str = Form("Adventure"),
    art_style: str = Form("Comic Book")
):

    # Comic panel prompts
    panel_prompts = [
        f"{character} standing at the edge of a mysterious forest, {setting}, {tone}, {art_style}",

        f"{character} walking deep inside the mysterious forest, {setting}, {tone}, {art_style}",

        f"{character} discovering a strange glowing object inside the forest, {setting}, {tone}, {art_style}",

        f"{character} uncovering an ancient hidden secret in the forest, {setting}, {tone}, {art_style}",

        f"{character} facing a dangerous final challenge in the forest, {setting}, {tone}, {art_style}",

        f"{character} returning home after the adventure, peaceful ending, {setting}, {tone}, {art_style}"
    ]

    descriptions = [
        f"{character} stood at the edge of a mysterious forest.",
        f"{character} slowly entered the deep woods.",
        f"{character} discovered something mysterious inside the forest.",
        f"{character} uncovered an ancient secret.",
        f"{character} faced the final challenge.",
        f"{character} returned home with a new story to tell."
    ]

    titles = [
        "The Forest's Edge",
        "Into the Deep Woods",
        "A Strange Discovery",
        "The Hidden Secret",
        "The Final Challenge",
        "A New Beginning"
    ]

    panels = []

    # Generate 6 images
    for i in range(6):

        image_url = generate_image(
            panel_prompts[i],
            i + 1
        )

        panels.append(
            {
                "number": i + 1,
                "title": titles[i],
                "image_url": image_url,
                "description": descriptions[i]
            }
        )

    return templates.TemplateResponse(
        request,
        "comic_preview.html",
        {
            "request": request,
            "panels": panels
        }
    )