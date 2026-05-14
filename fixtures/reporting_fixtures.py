import pytest
import allure

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # Capture screenshots and videos for failed (call) or broken (setup) tests
    if rep.when in ("setup", "call") and rep.failed:
        # Attempt to get the page from instantiated fixtures
        page = item.funcargs.get("page") or item.funcargs.get("unauthenticated_page")
        if page:
            try:
                # Attach Screenshot
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"Screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Attach Video if available
                if page.video:
                    # Force flush the video to disk by closing the context
                    page.context.close()
                    video_path = page.video.path()
                    allure.attach.file(
                        video_path,
                        name=f"Video_{item.name}",
                        attachment_type=allure.attachment_type.WEBM
                    )
            except Exception as e:
                print(f"Failed to attach screenshot/video to Allure: {e}")
