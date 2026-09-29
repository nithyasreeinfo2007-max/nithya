from typing import List, Optional
from pydantic import BaseModel, Field


class ComicRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    story_tone: str = "adventure"
    art_style: str = "comic book"
    num_panels: int = Field(default=4, ge=1, le=12)
    language: str = "English"


class PanelOutline(BaseModel):
    panel_number: int
    description: str
    characters: List[str] = []


class OutlineResponse(BaseModel):
    title: str
    outline: List[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int
    narration: str
    dialogue: List[str] = []
    image_prompt: str


class StoryResponse(BaseModel):
    title: str
    panels: List[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int
    narration: str
    dialogue: List[str] = []
    image_prompt: str
    image_url: Optional[str] = None


class ComicResponse(BaseModel):
    title: str
    panels: List[ComicPanel]