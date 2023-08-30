import os
import openai
import json


# Load instructions from JSON file
with open("instructions.json", "r") as f:
    INSTRUCTIONS = json.load(f)
    

class GPTService:
    """
    A service class for interacting with the GPT-3.5-turbo model via OpenAI API.
    
    Attributes:
        api_key (str): The API key for OpenAI. Sourced from environment variables.
        user_prompt (str): The prompt that the user provides for the model.
        response (str): The generated response from the GPT model.
        role_context (str): The context in which the GPT model operates.
        temperature (float): The randomness of the GPT model's output.
        md_code_format (str): Markdown instructions for code.
        md_table_format (str): Markdown instructions for tables.
        
    """
    
    def __init__(self, role_context='basic', prompt_context=True, md_table_format_style='pipes', temperature=0):
        """
        Initializes the GPTService class with parameters that control the prompt context and response output.
        
        Parameters:
            role_context (str, optional): The context in which the GPT model instance operates. Defaults to 'basic'.
                Options:
                    - 'basic': General-purpose context for general questions.
                    - 'api_explain': Context for explaining API documentation.
                    - 'code_help': Context for answering coding-related questions.
            temperature (float, optional): The randomness of the GPT model's output. Defaults to 0.
            prompt_context (bool, optional): Whether or not context (e.g. API documentation) is provided \
                for the prompt. Defaults to True.
            md_table_format_style (str, optional): The format in which to create a table. \
                Depending on the rendering application, some require a nested bulleted list, \
                    others require the pipe '|' character.  Defaults to 'pipes'.
        """
        
        # Initialization of attributes
        self.api_key = os.environ['OPENAI_API_KEY']
        self.user_prompt = ''
        self.response = ''
        self.role_context = role_context
        self.prompt_context = prompt_context
        self.temperature = temperature
        self.md_code_format = INSTRUCTIONS["code_formatting"]["md_code_format"]
        self.md_format_instruct = INSTRUCTIONS["general"]["md_format_instruct"]
        self.md_table_format_style = md_table_format_style
        self.md_table_format = self._set_md_table_format()
        
        openai.api_key = self.api_key
        
        self.context_handlers = {
            'basic': self._handle_basic,
            'api_explain': self._handle_api_explain,
            'code_help': self._handle_code_help,
        }
        
    def _set_md_table_format(self):
        """
        Sets the markdown table format based on the type.
        """
        if self.md_table_format_style == 'bullets':
            return INSTRUCTIONS["table_formatting"]["bullets"]
        elif self.md_table_format_style == 'pipes':
            return INSTRUCTIONS["table_formatting"]["pipes"]
        else:
            raise ValueError(f"Invalid md_table_format_style. Available styles: {list(INSTRUCTIONS['table_formatting'].keys())}.")

    def get_response(self, user_prompt):
        """Fetches the generated response from the GPT model based on the user prompt and context.
        
        Args:
            user_prompt (str): The prompt that the user provides for the model.
        
        Returns:
            str: The generated text from the GPT model.
        
        Notes:
            The behavior of this method changes based on the 'context' attribute:
                - 'basic': Provides general answers to questions.
                - 'api_explain': Provides explanations for API documentation.
                - 'code_help': Provides help for coding-related questions.
        """
        
        handler = self.context_handlers.get(self.role_context)
        if handler is None:
            raise ValueError(f"Invalid context: {self.role_context}")
        
        system_role, user_content = handler(user_prompt)
        
        model = "gpt-3.5-turbo"
        self.response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_content},
            ],
            temperature=self.temperature,
        )

        # Get the generated text
        generated_text = self.response['choices'][0]['message']['content']
        
        try:
            data = json.loads(generated_text)
            print(data)
            return data
        except json.JSONDecodeError:
            print(generated_text)
            return generated_text
        
    def _handle_basic(self, user_prompt):
        system_role = "You're a helpful assistant that answers my questions."
        user_content = user_prompt
        return system_role, user_content

    def _handle_api_explain(self, user_prompt):
        if self.prompt_context:
            prompt_preface = "For the following documentation, summarize if provided"
        else:
            prompt_preface = "For the following, provide me"
            
        api_explain_message = f"{prompt_preface} the description, parameters, attributes, 'returns', code examples \
        Provide a minimum of 3 examples, increasing in complexity, using various parameters."
        
        instructions = f"{api_explain_message}; {self.md_format_instruct}; {self.md_code_format}"
        user_content = f"{instructions}: {user_prompt}; {self.md_table_format}"
        system_role = "You're a helpful assistant and expert on analyzing python library documentation."
        return system_role, user_content

    def _handle_code_help(self, user_prompt):
        system_role = "You're a helpful assistant who answers coding language questions."
        user_content = f"{user_prompt}; {self.md_code_format}"
        return system_role, user_content

    def prompt(self, user_prompt=None):
        """
        Prompts the user for input and fetches the generated response from the GPT model.
        
        Parameters:
            user_prompt (str, optional): The prompt that the user may provide. \
                If None, user will be prompted for input.
        
        Returns:
            str: The generated text from the GPT model.
        
        """
        
        if user_prompt is None:
            self.user_prompt = input("Please provide a prompt: ")
        else:
            self.user_prompt = user_prompt
        return self.get_response(self.user_prompt)

