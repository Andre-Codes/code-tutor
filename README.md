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
gpt = GPTService(role_context="basic")
gpt.get_response("")
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

### API Explanation
```python
gpt = GPTService(role_context="api_explain")
response = gpt.get_response("")
print(response)
```
