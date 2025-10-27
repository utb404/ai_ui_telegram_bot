from pathlib import Path

import pytest
from gpn_qa_utils.ui.browser_launcher import BrowserLauncher
from playwright.sync_api import Page
from sample_ui.pages.pw_for_python_docs import PWForPythonDocs
from sample_ui.pages.pw_for_python_main import PWForPythonMain

BASE_DIR = Path(__file__).parent.parent
config_yml_path = BASE_DIR / "sample_ui" / "config_browser.yml"


@pytest.fixture(scope="function")
def browser() -> Page:
    launcher = BrowserLauncher(config_yml_path)
    new_page = launcher.create_page()
    yield new_page
    launcher.close()


@pytest.fixture(scope="function")
def pw_for_python_main(browser: Page) -> PWForPythonMain:
    """Главная страница сайта https://playwright.dev/python/."""
    return PWForPythonMain(browser)


@pytest.fixture(scope="function")
def pw_for_python_docs(browser: Page) -> PWForPythonDocs:
    """Страница с документацией https://playwright.dev/python/docs/."""
    return PWForPythonDocs(browser)
