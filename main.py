import gpt_service as gpt

test = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=False,
                            comment_level='detailed',
                            explain_level='comprehensive')

test.prompt = "pandas unstack function"

test.get_response(test.prompt, format_style='html')




code_help = gpt.GPTService(role_context='code_help',
                            temperature=0.2, comment_level='Exhaustive')
