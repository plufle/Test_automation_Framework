import pytest
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

def get_env():
    return {
        "email_user": os.getenv("EMAIL_USER"),
        "email_pass": os.getenv("EMAIL_PASS"),
    }

def load_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def config():
    base_config = load_config()
    env_config = get_env()
    base_config.update(env_config)
    return base_config
