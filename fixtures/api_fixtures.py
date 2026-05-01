import pytest
import json
from playwright.sync_api import Playwright

@pytest.fixture(scope="session")
def api_context(playwright: Playwright, config, global_auth_state):
    """
    Creates an API context using the token from the global auth state.
    """
    with open(global_auth_state, 'r') as f:
        state = json.load(f)
        
    token = None
    for origin in state.get('origins', []):
        for ls_item in origin.get('localStorage', []):
            if ls_item['name'] == 'auth_token':
                token = ls_item['value']
                break
        if token:
            break
            
    if not token:
        raise Exception("auth_token not found in storage state.")

    request_context = playwright.request.new_context(
        base_url=config["api_base_url"],
        extra_http_headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    yield request_context
    request_context.dispose()
