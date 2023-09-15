# CodeTutor - A Python Wrapper for GPT-3.5-turbo

** THIS README IS A WORK IN PROGRESS **

## Introduction

This Python class serves as an interface to the OpenAI GPT-3.5-turbo API. It allows for easy interaction with the model in various contexts such as basic Q&A, API explanation, coding assistance, and code refactoring.

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

## Usage

Initialize the `CodeTutor` class and then call its methods based on your use case. For example:

```python
api_explain = gpt.CodeTutor(role_context='api_explain',
                            temperature=0, 
                            prompt_context=True,
                            comment_level='verbose',
                            explain_level='comprehensive')
```



### Methods Description

#### `__init__(role_context, prompt_context, md_table_style, comment_level, temperature)`

Initializes the GPTService class with various settings.

#### Parameters
- `role_context` (str, optional): Defines the operational context of the GPT model.
- `prompt_context` (bool, optional): Indicates if additional context will be provided for the prompt.
- ... (continue for each method and parameter)

### Examples

## The 'code_help' role context
```python
code_help = gpt.CodeTutor(role_context='code_help',
                            comment_level='normal',
                            explain_level='comprehensive')
code_help.prompt = "using pandas compare two dataframes, and create a new one with the differences"
code_help.get_response(code_help.prompt, format_style='markdown')
```

### The 'pep8' role context, with assistant messages
(See this [notebook](https://github.com/Andre-Codes/code-tutor/blob/main/response_examples/chat_assistant_examples/chat_assistant.ipynb) for a full example with response output)
```python
# initiaite the class with the chosen role
fix_code = gpt.CodeTutor(role_context="pep8")

# create the prompt, save it to a unique variable
prompt_1 = """
counter=0
Num = 0.5
if 0 <= Num:
    if Num <= 1:
        for i in [0,2,4,6,8,10,12,14,16,18,20]:
            counter = counter + 1
            print(counter + ": " + i**2)
"""
# send the prompt and the response will be displayed in the output cell
# the response is also accessible from the response_content attribute
fix_code.get_response(prompt=prompt_1, format_style='markdown')

# create a second prompt to follow up the previous response
prompt2 = """
can you check again and confirm all the possible changes to 
the original code were made to conform to PEP8
"""

# save the first response to a variable
prompt1_response = fix_code.response_content
# create a list, alternate prompt and assistant message (response)
messages = [prompt_1, prompt_response, prompt2]
# send the messages and get another response
fix_code.get_response(prompt=messages, format_style='markdown')
```

