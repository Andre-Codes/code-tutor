import os
import openai
import json

class GPTService:
    """
    A service class for interacting with the GPT-3.5-turbo model via OpenAI API.
    
    Attributes:
        api_key (str): The API key for OpenAI. Sourced from environment variables.
        user_prompt (str): The prompt that the user provides for the model.
        response (str): The generated response from the GPT model.
        context (str): The context in which the GPT model operates.
        temperature (float): The randomness of the GPT model's output.
        md_code_instruct (str): Markdown instructions for code.
        api_explain_context (str): Instructions for API explanation.
        md_table_instruct (str): Markdown instructions for tables.
        
    """
    
    def __init__(self, context='basic', temperature=0):
        """Initializes the GPTService class with the given parameters.
        
        Args:
            context (str, optional): The context in which the GPT model operates. Defaults to 'basic'.
                Options:
                    - 'basic': General-purpose context for general questions.
                    - 'api_explain': Context for explaining API documentation.
                    - 'code_help': Context for answering coding-related questions.
            temperature (float, optional): The randomness of the GPT model's output. Defaults to 0.
        """
        
        self.api_key = os.environ['OPENAI_API_KEY']
        self.user_prompt = ''
        self.response = ''
        self.context = context
        self.temperature = temperature
        openai.api_key = self.api_key
        
        self.md_code_instruct = "Surround any python code with a single backtick"
        
        self.api_explain_context = "Using the following documentation, summarize \
            with fields, if available, for description, parameters, attributes, 'returns', code examples \
                Provide a minimum of 3 examples, increasing in complexity, using various parameters."
            
        self.md_table_instruct = "Format the parameters as a markdown table using \
            the following instructions: To add a table, use three or \
                more hyphens (---) to create each column header, and use pipes (|) \
                    to separate each column. For compatibility, you should also add \
                        a pipe on either end of the row."
                        
        self.context_handlers = {
            'basic': self._handle_basic,
            'api_explain': self._handle_api_explain,
            'code_help': self._handle_code_help,
        }

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
        
        handler = self.context_handlers.get(self.context)
        if handler is None:
            raise ValueError(f"Invalid context: {self.context}")
        
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
        system_role = "You're a helpful assistant and expert on analyzing python library documentation."
        instructions = f"{self.api_explain_context}; {self.md_code_instruct}"
        user_content = f"{instructions}: {user_prompt}; {self.md_table_instruct}"
        return system_role, user_content

    def _handle_code_help(self, user_prompt):
        system_role = "You're a helpful assistant who answers coding language questions."
        user_content = f"{user_prompt}; {self.md_code_instruct}"
        return system_role, user_content

    def prompt(self, user_prompt=None):
        """
        Prompts the user for input and fetches the generated response from the GPT model.
        
        Parameters:
            user_prompt (str, optional): The prompt that the user may provide. If None, user will be prompted for input.
        
        Returns:
            str: The generated text from the GPT model.
        
        """
        
        if user_prompt is None:
            self.user_prompt = input("Please provide a prompt: ")
        else:
            self.user_prompt = user_prompt
        return self.get_response(self.user_prompt)

