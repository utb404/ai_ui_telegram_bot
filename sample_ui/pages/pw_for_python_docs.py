from playwright.sync_api import Page

from gpn_qa_utils.ui.page_factory.link import Link
from gpn_qa_utils.ui.pages.base import BasePage


class PWForPythonDocs(BasePage):
    """Страница с документацией https://playwright.dev/python/docs/."""

    def __init__(self, page: Page):
        super().__init__(page, url="https://playwright.dev/python/docs/")

        self.link_frame = Link(page, strategy="by_text", value="Frame")
        self.link_file_chooser = Link(page, strategy="by_text", value="FileChooser")
        self.link_js_handle = Link(page, strategy="by_text", value="JSHandle")
