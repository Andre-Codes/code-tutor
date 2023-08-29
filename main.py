import gpt_service as gpt

api_helper = gpt.GPTService(role_context='api_explain',temperature=0.2, prompt_context=False)

api_helper.prompt = """
pandas .melt method
"""

answer = api_helper.get_response(api_helper.prompt)

print(answer)

