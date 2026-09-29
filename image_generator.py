from pathlib import Path
import os
import re
import uuid

from PIL import Image, ImageDraw

from app.config import settings


def safe_name(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value)
    value = value.strip("_")
    return value[:60] or "panel"


def create_placeholder(
    prompt: str,
    output_path: Path,
    panel_number: int,
):
    image = Image.new(
        "RGB",
        (
            settings.IMAGE_WIDTH,
            settings.IMAGE_HEIGHT,
        ),
        "white",
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (
            12,
            12,
            settings.IMAGE_WIDTH - 12,
            settings.IMAGE_HEIGHT - 12,
        ),
        outline="black",
        width=4,
    )

    draw.text(
        (35, 35),
        f"ComicCraft Panel {panel_number}",
        fill="black",
    )

    text = prompt[:350]

    lines = []
    current = ""

    for word in text.split():
        if len(current) + len(word) + 1 > 55:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()

    if current:
        lines.append(current)

    y = 90

    for line in lines[:10]:
        draw.text(
            (35, y),
            line,
            fill="black",
        )
        y += 30

    image.save(output_path, format="PNG")


def generate_hf_image(prompt: str):
    """
    Generate comic artwork using Hugging Face Inference API.
    """

    from huggingface_hub import InferenceClient

    hf_token = getattr(settings, "HF_TOKEN", None)

    if not hf_token:
        hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise RuntimeError(
            "HF_TOKEN is missing. "
            "Please add a valid Hugging Face token to .env"
        )

    model = getattr(
        settings,
        "IMAGE_MODEL",
        os.getenv(
            "IMAGE_MODEL",
            "black-forest-labs/FLUX.1-schnell",
        ),
    )

    provider = getattr(
        settings,
        "HF_PROVIDER",
        os.getenv("HF_PROVIDER", "auto"),
    )

    print("[ComicCraft] Connecting to Hugging Face...")
    print(f"[ComicCraft] Provider: {provider}")
    print(f"[ComicCraft] Model: {model}")

    try:
        client = InferenceClient(
            provider=provider,
            api_key=hf_token,
        )

        print("[ComicCraft] Sending image generation request...")

        image = client.text_to_image(
            prompt=prompt,
            model=model,
            width=settings.IMAGE_WIDTH,
            height=settings.IMAGE_HEIGHT,
            num_inference_steps=settings.IMAGE_STEPS,
        )

        if image is None:
            raise RuntimeError(
                "Hugging Face returned no image."
            )

        print(
            "[ComicCraft] Hugging Face image "
            "generated successfully."
        )

        return image

    except Exception as exc:
        print(
            f"[ComicCraft] Hugging Face error: {exc}"
        )

        raise RuntimeError(
            f"Hugging Face image generation failed: {exc}"
        ) from exc


def generate_image(
    prompt: str,
    panel_number: int,
):
    """
    Main image generation function used by main.py.
    """

    settings.ensure_directories()

    filename = (
        f"{panel_number:02d}_"
        f"{safe_name(str(uuid.uuid4()))}.png"
    )

    output_path = settings.panel_dir / filename

    enhanced_prompt = (
        f"{prompt}. "
        "Professional comic book illustration. "
        "Clear composition. "
        "Expressive characters. "
        "Consistent character appearance. "
        "Detailed environment. "
        "Cinematic lighting. "
        "High quality digital artwork. "
        "Clean line art. "
        "Rich colors. "
        "Comic book style. "
        "No written text. "
        "No speech bubbles. "
        "No watermark."
    )

    provider = settings.IMAGE_PROVIDER.lower().strip()

    print(
        f"[ComicCraft] Generating panel {panel_number} "
        f"using provider: {provider}"
    )

    if provider == "placeholder":

        create_placeholder(
            enhanced_prompt,
            output_path,
            panel_number,
        )

    elif provider == "hf_api":

        image = generate_hf_image(
            enhanced_prompt
        )

        image.save(
            output_path,
            format="PNG",
        )

    elif provider == "diffusers":

        raise RuntimeError(
            "Local Diffusers generation is disabled. "
            "Set IMAGE_PROVIDER=hf_api in .env."
        )

    else:

        raise RuntimeError(
            "Invalid IMAGE_PROVIDER. "
            "Use hf_api or placeholder."
        )

    if not output_path.exists():
        raise RuntimeError(
            f"Image file was not created: {output_path}"
        )

    print(
        f"[ComicCraft] Panel {panel_number} saved: "
        f"{output_path}"
    )

    return f"/static/panels/{filename}"