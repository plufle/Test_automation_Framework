import pytest
import allure

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(autouse=True)
def allure_attachments_on_failure(request):
    page = None
    if "page" in request.fixturenames:
        page = request.getfixturevalue("page")
        
    yield
    
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        if page:
            try:
                # Attach Screenshot
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"Screenshot_{request.node.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Attach Video if available
                if page.video:
                    video_path = page.video.path()
                    allure.attach.file(
                        video_path,
                        name=f"Video_{request.node.name}",
                        attachment_type=allure.attachment_type.WEBM
                    )
            except Exception as e:
                print(f"Failed to attach screenshot/video to Allure: {e}")
