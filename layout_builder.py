from typing import List

from app.schemas import (
    OutlineResponse,
    StoryResponse,
)


def build_comic_layout(
    outline: OutlineResponse,
    story: StoryResponse,
    image_paths: List[str],
):

    story_by_panel = {
        panel.panel_number: panel
        for panel in story.panels
    }

    layout = []

    for index, outline_panel in enumerate(
        outline.panels
    ):

        story_panel = story_by_panel.get(
            outline_panel.panel_number
        )

        if story_panel is None:
            raise ValueError(
                f"Missing story data for panel "
                f"{outline_panel.panel_number}"
            )

        layout.append(
            {
                "panel_number":
                    outline_panel.panel_number,

                "title":
                    story_panel.title
                    or outline_panel.title,

                "image_path":
                    image_paths[index],

                "scene_description":
                    story_panel.scene_description
                    or outline_panel.scene_description,

                "caption":
                    story_panel.caption,

                "narration":
                    story_panel.narration,

                "dialogue":
                    story_panel.dialogue,

                "image_prompt":
                    outline_panel.image_prompt,
            }
        )

    return layout