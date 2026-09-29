from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# ============================================================
# Base Project Directory
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    # ========================================================
    # Application
    # ========================================================

    APP_NAME: str = "ComicCraft"

    # ========================================================
    # API Keys
    # ========================================================

    GEMINI_API_KEY: str = ""
    HF_TOKEN: str = ""

    # ========================================================
    # Gemini Models
    # ========================================================

    GEMINI_OUTLINE_MODEL: str = "gemini-2.5-flash"
    GEMINI_STORY_MODEL: str = "gemini-2.5-pro"

    # ========================================================
    # Image Generation
    # ========================================================

    IMAGE_PROVIDER: str = "hf_api"

    IMAGE_MODEL: str = "black-forest-labs/FLUX.1-schnell"

    HF_PROVIDER: str = "fal-ai"

    # ========================================================
    # Comic Settings
    # ========================================================

    NUM_PANELS: int = 6

    IMAGE_WIDTH: int = 768
    IMAGE_HEIGHT: int = 512

    IMAGE_STEPS: int = 4

    # ========================================================
    # Local Image Generation
    # ========================================================

    LOCAL_IMAGE_MODEL: str = "runwayml/stable-diffusion-v1-5"

    LOCAL_DEVICE: str = "auto"

    # ========================================================
    # Environment Configuration
    # ========================================================

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ========================================================
    # Static Directory
    # ========================================================

    @property
    def static_dir(self) -> Path:
        """
        Main static directory.

        Images and CSS are served from:

        app/static/
        """

        return BASE_DIR / "app" / "static"

    # ========================================================
    # Comic Panels Directory
    # ========================================================

    @property
    def panel_dir(self) -> Path:
        """
        Directory where generated comic panels are saved.

        app/static/panels/
        """

        return self.static_dir / "panels"

    # ========================================================
    # Export Directory
    # ========================================================

    @property
    def export_dir(self) -> Path:
        """
        Directory where exported files are saved.

        app/static/exports/
        """

        return self.static_dir / "exports"

    # ========================================================
    # Create Required Directories
    # ========================================================

    def ensure_directories(self):
        """
        Create required folders automatically if
        they do not already exist.
        """

        self.static_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.panel_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.export_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# Global Settings Object
# ============================================================

settings = Settings()