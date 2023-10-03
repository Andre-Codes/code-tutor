# CodeTutor - An AI Teacher for Coding

** THIS README IS A WORK IN PROGRESS **

## Introduction

Context-based AI assistant for customized lessons on various coding related concepts. Enjoy real-time responses after choosing from a variety of specialized contexts, including API explanation for in-depth library insights, general code assistance with suggestions and real-world code examples, code conversion for multilingual coding (Python to C++, SQL to Pandas, etc.), and PEP 8 standardization to refine and polish your code. Get precise, tailored lessons and solutions to your coding queries with ease.

## Table of Contents

- [Introduction](#introduction)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Methods Description](#methods-description)
- [Examples](#examples)

## Installation and Setup

#### Jupyter Notebook module
To use CodeTutor from within a Jupyter Notebook you must include the 

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

