import gpt_service as gpt

numpy_api = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=False,
                            comment_level='detailed',
                            explain_level='child-level')

numpy_api.prompt = "pandas .join function"

numpy_api.get_response(numpy_api.prompt)

numpy_api.md_table_style



code_help = gpt.GPTService(role_context='code_help',
                            temperature=0.2, comment_level='Exhaustive')

code_help.prompt = "how do i generate a plot that puts an arrow at the vertex"

code_help.get_response(code_help.prompt)

import numpy as np

np.eye