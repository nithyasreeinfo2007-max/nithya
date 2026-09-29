# ComicCraft

ComicCraft is a Generative AI based comic creation application.

## Features

- Generate comic story outlines using Gemini
- Generate comic stories and dialogue
- Generate comic panel images
- Create multi-panel comic layouts
- Preview generated comics
- Export comics as PDF
- FastAPI backend
- HTML/CSS frontend

## Project Structure

```text
ComicCraft/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
│
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── panels/
│   └── exports/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md