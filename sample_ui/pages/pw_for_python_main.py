from playwright.sync_api import Page

from gpn_qa_utils.ui.page_factory.button import Button
from gpn_qa_utils.ui.page_factory.component_list import ComponentList
from gpn_qa_utils.ui.page_factory.input import Input
from gpn_qa_utils.ui.pages.base import BasePage


class PWForPythonMain(BasePage):
    """Главная страница сайта https://playwright.dev/python/."""

    def __init__(self, page: Page):
        super().__init__(page, url="https://playwright.dev/python/")

        self.button_search = Button(
            page, strategy="locator", selector=".DocSearch", allure_name="Поле для поиска"
        )

        self.search_input_field = Input(
            page,
            strategy="locator",
            selector=".DocSearch-Input",
            allure_name="Ввод текста для поиска",
        )

        self.button_first_search_value = Button(
            page,
            strategy="locator",
            selector=".DocSearch-Hit#docsearch-item-0",
            allure_name="Первый результат поиска",
        )

        self.button_get_started = Button(
            page, strategy="locator", selector=".getStarted_Sjon", allure_name="Кнопка Начать"
        )

        self.button_top_api = Button(
            page,
            strategy="locator",
            selector="a.navbar__item.navbar__link[href='/python/docs/api/class-playwright']",
            allure_name="Кнопка API",
        )

        self.button_top_community = Button(
            page,
            strategy="locator",
            selector="a.navbar__item.navbar__link[href='/python/community/welcome']",
            allure_name="Кнопка Community",
        )

        self.button_top_docs = Button(
            page,
            strategy="locator",
            selector="a.navbar__item.navbar__link[href='/python/docs/intro']",
            allure_name="Кнопка Docs",
        )

        self.button_bottom_getting_started = Button(
            page,
            strategy="by_role",
            role="link",
            value="Docs",
            allure_name="Кнопка Docs",
        )

        self.select_language_menu = ComponentList(
            page,
            selector=".navbar__link",
            allure_name="Элементы меню в заголовке"
        )

        self.select_language_list = ComponentList(
            page,
            selector=".dropdown__link",
            allure_name="Выбор языка программирования"
        )
        self.button_get_started = Button(
            page,
            strategy="by_text",
            value="Get started",
            allure_name="Кнопка Get started",
        )


    def input_search_field(self):
        """Вводит значение в поле поиска."""
        self.button_search.click()
        self.search_input_field.fill(text="get_by_role")
        self.search_input_field.click()

    def hover_language_menu(self):
        """Наводит мышь на меню выбора языка программирования."""

        self.select_language_menu.item(2).get_element().hover()
        self.select_language_list.item(0).check_visible()
