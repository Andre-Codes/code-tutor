import gpt_service as gpt

pandas_api = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=False, 
                            md_table_style='pipes',
                            comment_level='Basic')

pandas_api.prompt = "pandas .resample function"

pandas_api.get_response(pandas_api.prompt)

pandas_api.md_table_style



code_help = gpt.GPTService(role_context='code_help',
                            temperature=0.2, comment_level='Pedagogical')

code_help.prompt = "i need to reverse a string and then select the middle character, If odd number of characters, select middle two"

code_help.get_response(code_help.prompt)
