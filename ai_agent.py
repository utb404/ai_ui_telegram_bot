import asyncio
import os
import pathlib

from browser_use import Agent
from browser_use.llm import ChatDeepSeek
from dotenv import load_dotenv

load_dotenv()


SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
agent_dir = SCRIPT_DIR / 'file_system'
agent_dir.mkdir(exist_ok=True)
conversation_dir = agent_dir / 'conversations' / 'conversation'
print(f'Agent logs directory: {agent_dir}')

# # extend_system_message = """
# # Наиболее важные правила, их нельзя нарушать:
# # 1. Твоя роль - Senior QA Engineer.
# # 2. Твоя задача - проверка функциональности по тест-кейсам или текстовому описанию сценария.
# # 3. Твоя задача - проверить что тест-кейс проходит.
# # 4. На выходе должна быть оценка что тест-кейс или набор тест-кейсов прошел.
# # 5. При негативном выполнении тест-кейса, должна быть оценка что тест-кейс не прошел и предположительная причина.
# # 6. При негативном выполнении тест-кейса, должен быть сформирован баг-репорт.
# # """
#
# extend_system_message = """
# Наиболее важные правила, их нельзя нарушать:
# 1. Твоя роль - Senior Automation QA Engineer.
# 2. Твоя задача - разработка автотестов по тест-кейсам или текстовому описанию сценария.
# 3. Твоя задача - проверить что тест-кейс проходит и разработать для него автотест.
# 4. Для разработки автотестов необходимо использовать следующий стек: Python, Playwright, pytest.
# 5. На выходе должна быть оценка что тест-кейс или набор тест-кейсов прошел.
# 6. При негативном выполнении тест-кейса, должна быть оценка что тест-кейс не прошел и предположительная причина.
# 7. При негативном выполнении тест-кейса, должен быть сформирован баг-репорт.
# 8. В результате помимо оценки должен быть сформирован автотест.
# 9. Код автотеста должен быть представлен только в виде вывода, а не в виде файлов.
# 10. Демонстрируй на каждом шаге то, что представлено в devtools браузера во вкладке Network.
# 11. В ответе предоставь список маппинга шагов тест-кейса и вызываемых запросов в Network.
# """

deepseek_api_key = os.getenv('DEEPSEEK_TOKEN')
if deepseek_api_key is None:
	print('Make sure you have DEEPSEEK_API_KEY:')
	print('export DEEPSEEK_API_KEY=your_key')
	exit(0)


async def ai_generate(prompt: str):
	llm = ChatDeepSeek(
		base_url='https://api.deepseek.com/v1',
		model='deepseek-chat',
		api_key=deepseek_api_key,
	)

	agent = Agent(
		task=prompt,
		llm=llm,
		use_vision=False,
		# extend_system_message=prompt,
		llm_timeout=300,
		save_conversation_path=str(conversation_dir),
		file_system_path=str(agent_dir / 'fs'),
	)
	agent_history = await agent.run()
	# print(f'Final result: {agent_history.final_result()}', flush=True)
	return agent_history.final_result()

# asyncio.run(generate())

# task = 'Разработай автотест, который будет проходить следующий тест-кейс:'
# '1. Открыть страницу https://playwright.dev'
# '2. Выберет язык Python'
# '3. Откроет документацию'
# '4. В документации откроет вкладку Writing tests'
# '5. Убедится что вкладка Writing tests открыта'