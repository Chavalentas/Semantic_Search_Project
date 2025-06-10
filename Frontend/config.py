from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    """The configuration file.
    """
    project_path: Path = Path(__file__).resolve().parent
    app_settings_path: Path = project_path.joinpath("app_settings.json")
    backend_url = "https://semantic-search-project-backend.onrender.com" #"http://127.0.0.1:8000"


