import gpt_service as gpt

system_role = "You're a helpful assistant and expert on analyzing python library documentation"

ai = gpt.GPTService(system_role=system_role, temperature=0.2)

ai.prompt = "Summarize sklearn ordinal encoder, respond in JSON format with fields \
for description, parameters, attributes, examples. Use markdown for headings and code"

answer = ai.get_response(ai.prompt)

print(answer)


