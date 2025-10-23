import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".settings")


@dataclass
class Settings:
    url_prod: str = os.getenv("url_prod")
    url_dev: str = os.getenv("url_dev")
    resource_id_prod: str = os.getenv("resource_id_prod")
    resource_id_dev: str = os.getenv("resource_id_dev")
    tenant_id: str = os.getenv("tenant_id")
    # Add more fields as needed


settings = Settings()
