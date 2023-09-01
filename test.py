import gpt_service as gpt

# Example using the 'api_explain' context and requiring
# a response in HTML format
api_help = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=True,
                            comment_level='detailed',
                            explain_level='comprehensive')

api_help.prompt = "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html"

api_help.get_response(api_help.prompt, format_style='html')


# Example using the 'code_help' context
code_help = gpt.GPTService(role_context='code_help',
                           comment_level='detailed',
                           explain_level='normal')

code_help.prompt = "using the pandas styler creating a function to color the value above the average for a column in a dataframe"

code_help.get_response(code_help.prompt, format_style='html')
