import allure


@allure.epic("Сайт playwright.dev")
@allure.feature("Раздел Playwright for Python")
@allure.story("Основной функционал")
class TestMainPage:
    @allure.title("Проверка поля поиска документации")
    def test_input_search(self, pw_for_python_main):
        with allure.step("Откроем страницу"):
            pw_for_python_main.open()

        with allure.step("Введем текст в поле поиска документации"):
            pw_for_python_main.input_search_field()

        with allure.step("Перейдем по первому попавшемуся результату поиска"):
            pw_for_python_main.button_first_search_value.click()

    @allure.title("Проверка кнопки GetStarted")
    def test_get_started(self, pw_for_python_main):
        with allure.step("Откроем страницу"):
            pw_for_python_main.open()

        with allure.step("Нажмем на кнопку Начать"):
            pw_for_python_main.button_get_started.click()

    @allure.title("Проверка главного меню")
    def test_top_menu(self, pw_for_python_main):
        with allure.step("Откроем страницу"):
            pw_for_python_main.open()

        with allure.step("Перейдем на страницу Docs"):
            pw_for_python_main.button_top_docs.click()

        with allure.step("Перейдем на страницу API"):
            pw_for_python_main.button_top_api.click()

        with allure.step("Перейдем на страницу Community"):
            pw_for_python_main.button_top_community.click()

    @allure.title("Проверка нижнего меню")
    def test_bottom_menu(self, pw_for_python_main):
        with allure.step("Откроем страницу"):
            pw_for_python_main.open()

        with allure.step("Перейдем на страницу Getting started"):
            pw_for_python_main.button_bottom_getting_started.click()

        with allure.step("Перейдем на страницу API reference"):
            pw_for_python_main.button_top_api.click()

    @allure.title("Проверка выбора языка программирования")
    def test_select_language(self, pw_for_python_main):
        with allure.step("Откроем страницу"):
            pw_for_python_main.open()

        with allure.step("Выберем язык Node.js по индексу"):
            pw_for_python_main.hover_language_menu()
            pw_for_python_main.select_language_list.item(1).click()
            assert pw_for_python_main.select_language_menu.item(2).get_text() == "Node.js"

        with allure.step("Выберем язык Java по тексту"):
            pw_for_python_main.hover_language_menu()
            pw_for_python_main.select_language_list.item(with_text="Java").click()
            assert pw_for_python_main.select_language_menu.item(2).get_text() == "Java"

        with allure.step("Выберем язык Python по вхождению текста"):
            pw_for_python_main.hover_language_menu()
            pw_for_python_main.select_language_list.item(contains_text="Pyt").click()
            assert pw_for_python_main.select_language_menu.item(2).get_text() == "Python"


@allure.epic("Сайт playwright.dev")
@allure.feature("Раздел Playwright for Python")
@allure.story("Документация")
class TestDocPage:
    @allure.title("Проверка панели навиграции по документам")
    def test_navigation_tab(self, pw_for_python_docs):
        with allure.step("Откроем страницу"):
            pw_for_python_docs.open()

        with allure.step("Перейдем в раздел Фрейм"):
            pw_for_python_docs.link_frame.click()

        with allure.step("Перейдем в раздел JSHandle"):
            pw_for_python_docs.link_js_handle.click()

        with allure.step("Перейдем в раздел FileChooser"):
            pw_for_python_docs.link_file_chooser.click()
@allure.epic("Сайт playwright.dev")
@allure.feature("Скриншот-тесты")
class TestScreenShot:
    @allure.title("Проверка функции создания/сравнения скриншотов")
    def test_screenshot(self, pw_for_python_main):
        pw_for_python_main.open()
        pw_for_python_main.button_get_started.compare_screenshots()
