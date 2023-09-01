import gpt_service as gpt

# Example using the 'api_explain' context and requiring
# a response in HTML format
test = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=False,
                            comment_level='detailed',
                            explain_level='comprehensive')

test.prompt = "pandas pivot function"

test.get_response(test.prompt, format_style='html')


# Example using the 'code_help' context
code_help = gpt.GPTService(role_context='code_help', comment_level='exhaustive')
