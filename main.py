import gpt_service as gpt

pandas_api = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=False, 
                            md_table_format_style='pipes')

pandas_api.prompt = "pandas .pivot function"

pandas_api.get_response(pandas_api.prompt)


code_help = gpt.GPTService(role_context='code_help',
                            temperature=0.2)

code_help.prompt = "using a lambda function with the pandas .agg method"

code_help.get_response(code_help.prompt)