import os



def get_python_code_from_directory(directory_path: str) -> str:
    code_pieces = []
    for root, dirs, files in os.walk(directory_path):
        # Добавляем заголовок для текущей директории
        code_pieces.append(f"# Директория: {root}")
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    code_pieces.append(f"# Файл: {file}\n{content}\n")
    return "\n".join(code_pieces)


def form_prompt(test_case: str) -> str:
    sample_code = get_python_code_from_directory('sample_ui')

    # prompt = f"""
    #     Ты — опытный инженер по автоматизации тестирования. Твоя задача — написать автотесты на Python с использованием стеков Playwright, pytest и allure.
    #
    #     Ниже я предоставлю тебе три блока информации:
    #
    #     1. **Sample-проект (код проекта):**
    #     <<<PROJECT_START>>>
    #     {sample_code}
    #     <<<PROJECT_END>>>
    #
    #     2. **Тест-кейс для реализации:**
    #     <<<TESTCASE_START>>>
    #     {test_case}
    #     <<<TESTCASE_END>>>
    #
    #     3. **Требования к тестам:**
    #     - Код автотестов должен соответствовать sample-проекту - это очень важно!
    #     - Использовать `pytest` как тестовый раннер.
    #     - Для браузерных действий использовать `Playwright` (браузер chromium, запуск по умолчанию в headless-режиме).
    #     - Добавить работу с `allure` (декораторы и шаги для детальных отчетов).
    #     - Код автотестов должен быть структурирован (Page Object Model, фикстуры pytest для браузера).
    #     - В итоговом решении:
    #       - использовать `allure.step` для каждого ключевого шага теста;
    #       - использовать понятные имена функций и классов;
    #       - добавить ассерты, которые проверяют ожидаемый результат из тест-кейса.
    #
    #     На основе этой информации выполни проверку по тест-кейсу и сгенерируй:
    #     - Код автотеста, реализующий указанный тест-кейс.
    #
    #     Предусловия и шаги с ожидаемыми результатами в тест-кейсе описаны в полях "preconditions" и "actions".
    #     Выводи готовый рабочий код в отдельных блоках markdown.
    #     В качестве ответа дай оценку успешности прохождения тест-кейса и готовый рабочий код.
    #     При негативном выполнении тест-кейса, должна быть оценка что тест-кейс не прошел и предположительная причина.
    #     При негативном выполнении тест-кейса, должен быть сформирован баг-репорт.
    #     ВАЖНО: ты не должен создавать новые файлы, ты должен только сгенеририровать код в markdown.
    # """

    prompt = f"""You are an experienced test automation engineer. Your task is to write automated tests in Python using the Playwright, pytest, and allure stacks.
    I will provide you with three blocks of information:
    
    1. **Sample project (project code):**  
    <<<PROJECT_START>>>  
    {sample_code}  
    <<<PROJECT_END>>>
    
    2. **Test case for implementation (in JSON format):**  
    <<<TESTCASE_START>>>  
    {test_case}  
    <<<TESTCASE_END>>>
    
    3. **Requirements for the tests:**  
    - The test code must strictly follow the style and patterns of the sample project. This is very important!  
    - Use `pytest` (specify version if needed) as the test runner.  
    - Use `Playwright` for browser interactions (Chromium browser, default headless mode).  
    - Structure code according to the Page Object Model (POM) design pattern.  
    - Use pytest fixtures to manage browser lifecycle and any reusable setup.  
    - Integrate `allure` for detailed reporting, using decorators and `allure.step` for every key step in the test.  
    - Provide meaningful and descriptive names for functions, classes, and variables. Include docstrings where appropriate.  
    - Include assertions that verify expected results specified in the test case.  
    - Implement error and exception handling in tests to increase stability.  
    - When the test case fails, generate a bug report following this template:  
      - Brief description of the issue  
      - Steps to reproduce  
      - Expected result  
      - Actual result  
    - Respond with all generated code in markdown code blocks only. Do not create or mention file structures or filenames.  
    - Add comments in the code to clarify key steps and logic.
    
    Based on this information, perform the following:
    
    - Review the given test case using the sample project context.  
    - Generate ready-to-run Python code for the automated test implementing the test case.  
    - Provide an assessment of whether the test case will pass or fail.  
    - If the test case fails, provide a plausible reason for failure and include a bug report as specified above.
    
    Important: All output must be in Russian. Only the prompt is in English to improve AI agent comprehension and strictness.
    
    """


    return prompt
