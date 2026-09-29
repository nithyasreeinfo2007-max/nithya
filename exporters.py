from datetime import datetime
from pathlib import Path
import re

from fpdf import FPDF

from app.config import settings


def clean_text(text: str) -> str:
    return re.sub(
        r"[^\x00-\xFF]",
        "",
        text or "",
    )


def save_pdf(
    layout: list[dict],
    title: str = "ComicCraft Comic",
):

    settings.ensure_directories()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"comiccraft_{timestamp}.pdf"
    )

    output_path = (
        settings.export_dir / filename
    )

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        pdf.multi_cell(
            0,
            10,
            clean_text(
                f"Panel {panel['panel_number']}: "
                f"{panel['title']}"
            ),
        )

        image_file = (
            settings.static_dir
            / Path(
                panel["image_path"]
                .replace("/static/", "")
            )
        )

        if image_file.exists():

            max_width = 175

            x = (
                210 - max_width
            ) / 2

            pdf.image(
                str(image_file),
                x=x,
                w=max_width,
            )

        pdf.ln(5)

        pdf.set_font(
            "Helvetica",
            "I",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            clean_text(
                panel["scene_description"]
            ),
        )

        pdf.ln(3)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            "Caption",
        )

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            clean_text(
                panel["caption"]
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            "Narration",
        )

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            clean_text(
                panel["narration"]
            ),
        )

        if panel["dialogue"]:

            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "B",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                "Dialogue",
            )

            pdf.set_font(
                "Helvetica",
                "",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                clean_text(
                    panel["dialogue"]
                ),
            )

    pdf.output(
        str(output_path)
    )

    return (
        f"/static/exports/{filename}"
    )