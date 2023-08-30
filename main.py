import gpt_service as gpt

api_helper = gpt.GPTService(role_context='api_explain',
                            temperature=0.2, 
                            prompt_context=False, 
                            md_table_format_style='pipes')

api_helper.prompt = """
pandas .unstack method
"""

api_helper.get_response(api_helper.prompt)


api_helper_2 = gpt.GPTService(role_context='api_explain',
                            temperature=0.2, 
                            prompt_context=True, 
                            md_table_format_style='pipes')

api_helper_2.prompt = """
def unstack(level: Level=-1, fill_value=None)
Pivot a level of the (necessarily hierarchical) index labels.

Returns a DataFrame having a new level of column labels whose inner-most level consists of the pivoted index labels.

If the index is not a MultiIndex, the output will be a Series (the analogue of stack when the columns are not a MultiIndex).

Parameters
level : int, str, or list of these, default -1 (last level)
    Level(s) of index to unstack, can pass level name.
fill_value : int, str or dict
    Replace NaN with this value if the unstack produces missing values.

Returns
Series or DataFrame

See Also
DataFrame.pivot : Pivot a table based on column values.
DataFrame.stack : Pivot a level of the column labels (inverse operation
    from unstack).

Notes
Reference the user guide <reshaping.stacking> for more examples.
"""

api_helper_2.get_response(api_helper_2.prompt)