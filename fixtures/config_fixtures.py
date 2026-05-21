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

def load_config(env):
    with open("config/config.yaml") as f:
        data = yaml.safe_load(f)
        
    config = data.get("default", {})
    env_data = data.get(env, {})
    config.update(env_data)
    
    return config

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    base_config = load_config(env)
    env_config = get_env()
    base_config.update(env_config)
    return base_config
