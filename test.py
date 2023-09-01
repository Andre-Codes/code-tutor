import gpt_service as gpt

# Example using the 'api_explain' context and requiring
# a response in HTML format
api_help = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=False,
                            comment_level='detailed',
                            explain_level='comprehensive')

api_help.prompt = "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html"

api_help.get_response(api_help.prompt, format_style='html')

api_help.response_file


# Example using the 'code_help' context
code_help = gpt.GPTService(role_context='code_help',
                           comment_level='detailed',
                           explain_level='comprehensive')

code_help.prompt = "creating a lambda function to convert every other letter to upper case in a dataframe column"

code_help.get_response(code_help.prompt, format_style='html')
