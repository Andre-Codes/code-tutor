# GPTService - A Python Wrapper for GPT-3.5-turbo

** THIS README IS A WORK IN PROGRESS **

## Introduction

This Python class serves as an interface to the OpenAI GPT-3.5-turbo API. It allows for easy interaction with the model in various contexts such as basic Q&A, API explanation, and coding assistance.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Methods Description](#methods-description)
- [Examples](#examples)

## Prerequisites

- Python 3.x
- OpenAI API Key

## Installation and Setup

1. Clone this repository.
2. Install the required packages.
3. Add your OpenAI API key to the environment variables.

## Usage

Initialize the `GPTService` class and then call its methods based on your use case. For example:

```python
api_explain = gpt.GPTService(role_context='api_explain',
                            temperature=0, 
                            prompt_context=True,
                            comment_level='verbose',
                            explain_level='comprehensive')
api_explain.prompt = "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html"
api_explain.get_response(api_explain.prompt, format_style='html')
```

```python
code_help = gpt.GPTService(role_context='code_help',
                            comment_level='normal',
                            explain_level='comprehensive')
code_help.prompt = "using pandas compare two dataframes, and create a new one with the differences"
code_help.get_response(code_help.prompt, format_style='markdown')
```

## Methods Description

### `__init__(role_context, prompt_context, md_table_style, comment_level, temperature)`

Initializes the GPTService class with various settings.

#### Parameters
- `role_context` (str, optional): Defines the operational context of the GPT model.
- `prompt_context` (bool, optional): Indicates if additional context will be provided for the prompt.
- ... (continue for each method and parameter)

## Examples

### Basic Usage
```python
gpt = GPTService(role_context="basic")
response = gpt.get_response("")
print(response)
```
### ======= Example Result =======

The below example is as is, no changes made to the API response.

### =========================

# Comparing and Creating a New DataFrame with Differences using Pandas

## Summary
The question is about comparing two DataFrames using the pandas library in Python and creating a new DataFrame that contains the differences between the two original DataFrames.

## Process Explanation
To compare two DataFrames and create a new one with the differences, you can follow these steps:

1. Import the necessary libraries:
```python
import pandas as pd
```

2. Create two DataFrames to compare:
```python
df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'A': [1, 2, 4], 'B': [4, 5, 7]})
```

3. Use the `compare` method from pandas to compare the two DataFrames:
```python
comparison_result = df1.compare(df2)
```

4. The `comparison_result` will be a new DataFrame that contains the differences between the two original DataFrames. It will have three columns: `self`, `other`, and `diff`. The `self` column represents the values from the first DataFrame (`df1`), the `other` column represents the values from the second DataFrame (`df2`), and the `diff` column represents the differences between the two values.

5. You can access the differences by filtering the `diff` column:
```python
differences = comparison_result['diff']
```

6. If you want to create a new DataFrame with only the differences, you can use the `dropna` method to remove rows with no differences:
```python
new_df = differences.dropna()
```

7. The `new_df` will be a DataFrame that contains only the rows with differences between the two original DataFrames.

## Examples

### Example 1:
```python
import pandas as pd

df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'A': [1, 2, 4], 'B': [4, 5, 7]})

comparison_result = df1.compare(df2)
differences = comparison_result['diff']
new_df = differences.dropna()

print(new_df)
```
Output:
```
     A    B
2  3.0  6.0
```

### Example 2:
```python
import pandas as pd

df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

comparison_result = df1.compare(df2)
differences = comparison_result['diff']
new_df = differences.dropna()

print(new_df)
```
Output:
```
Empty DataFrame
Columns: [A, B]
Index: []
```

### Example 3:
```python
import pandas as pd

df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'A': [4, 5, 6], 'B': [1, 2, 3]})

comparison_result = df1.compare(df2)
differences = comparison_result['diff']
new_df = differences.dropna()

print(new_df)
```
Output:
```
     A    B
0  1.0  4.0
1  2.0  5.0
2  3.0  6.0
```

## Sources
- [pandas documentation](https://pandas.pydata.org/docs/)
- [GeeksforGeeks - Compare two Pandas DataFrames for differences](https://www.geeksforgeeks.org/compare-two-pandas-dataframes-for-differences/)
- [Real Python - How to Compare Values in Two Pandas DataFrames](https://realpython.com/pandas-compare-rows/)

#### ======= End of Example Result =======
