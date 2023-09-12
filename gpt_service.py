import os
import openai
import json
import datetime
from IPython.display import display, HTML, Markdown

# Load instructions from JSON file
with open("instructions.json", "r") as f:
    INSTRUCTIONS = json.load(f)

class GPTService:
    """
    A service class for interacting with the GPT-3.5-turbo model via the OpenAI API.
    
    Attributes:
        api_key (str): The API key for OpenAI, sourced from environment variables.
        user_prompt (str): The prompt that the user provides for the model.
        response (str): The generated response from the GPT model.
        role_context (str): The context in which the GPT model operates. 
                            Valid options are sourced from INSTRUCTIONS.json.
        temperature (float): The randomness of the GPT model's output.
        md_code_format (str): Markdown instructions for code formatting.
        md_table_format (str): Markdown instructions for tables.
        
    Methods:
        __init__(role_context, prompt_context, md_table_style, comment_level, temperature):
            Initializes the class attributes based on provided parameters.
            
        _set_md_table_format():
            Sets the Markdown table format based on the type.
        
        get_response(user_prompt):
            Fetches a response from the GPT model based on the user's prompt and context.
            
        _handle_basic(user_prompt):
            Context handler for 'basic' role_context.
            
        _handle_api_explain(user_prompt):
            Context handler for 'api_explain' role_context.
            
        _handle_code_help(user_prompt):
            Context handler for 'code_help' role_context.
            
        prompt(user_prompt):
            Prompts the user for input and fetches the GPT model's response.
            
    Comment Levels:
        For role_context='api_explain':
            - "Basic", "Thorough", "Comprehensive", "Advanced", "Pedagogical", "Technical"
        
        For role_context='code_help':
            - "Basic", "Moderate", "Detailed", "Verbose", "Exhaustive", "Pedagogical"
    """
    
    # Class variables
    DISPLAY_MAPPING = { # mappings for IPython.display function names
        'html': HTML,
        'markdown': Markdown
    }
    
    MD_TABLE_STYLE = "pipes" # default format for markdown tables
    
    def __init__(
        self, 
        role_context=None, 
        prompt_context=None, 
        comment_level=None, 
        explain_level=None, 
        temperature=None):
        """
        Initializes the GPTService class with various settings.

        # Parameters
        ----------
        role_context : (str, optional): 
            Defines the operational context of the GPT model.
            Defaults to 'basic'.
            
            Options include:
                - 'basic': General-purpose context for answering questions.
                - 'api_explain': For summarizing and explaining API documentation. If the `prompt_context` parameter is set to `True`,
                    this will enable the passing of entire API documentation as the prompt, ensuring up-to-date information in the response.
                - 'code_help': For coding-related help.
                
        prompt_context : (bool, optional): 
            Indicates if additional context (i.e. API documentation) will be provided for the prompt. Defaults to False.
            
        md_table_style (str, optional): 
            Specifies the Markdown table format. Defaults to 'pipes'.
            Options:
                - 'bullets': Use nested bulleted lists for tables.
                - 'pipes': Use pipe characters to separate table cells.
                
        comment_level : (str, optional):
            Specifies the level of commenting for either 'api_explain' or 'code_help' role_contexts.
            Available options are based on the value of role_context. Defaults to 'Basic' for 'api_explain' and 'code_help'.
            
        temperature : (float, optional):
            Controls the randomness of the GPT model's output. Lower values make the output more deterministic. Defaults to 0.
        """
        
        # Initialization of attributes
        self.api_key = os.environ['OPENAI_API_KEY']
        openai.api_key = self.api_key
        self.user_prompt = ''
        self.response = ''
        # Validate role_context against available contexts in JSON
        available_role_contexts = INSTRUCTIONS.get('role_contexts', {}).keys()
        self.role_context = role_context if role_context in available_role_contexts else 'basic'

        self.prompt_context = prompt_context if prompt_context is not None else False  # Default to False
        # self.md_table_style = md_table_style or INSTRUCTIONS.get('table_formatting', {}).get('default', 'pipes')
        # Get available comment and explain levels or set default to 'normal'
        comment_levels = INSTRUCTIONS['comment_levels']
        self.comment_level = comment_level if comment_level in comment_levels \
            or comment_level is None  else 'normal'
        explain_levels = INSTRUCTIONS['explain_levels']
        self.explain_level = explain_level if explain_level in explain_levels \
            or explain_level is None  else 'concise'
        
        self.temperature = temperature or 0  # Default to 0

        # Load remaining settings from JSON
        # self.md_table_format = self._set_md_table_format()
        
        # self.context_handlers = (
        #     {context: getattr(self, f'_handle_{context}') for context in INSTRUCTIONS.get('role_contexts', {})}
        # )
        
        # Set file extensions based on response format
        self.file_exts = {
            "markdown": "md",
            "html": "html"
        }
    
    def set_md_table_style(self, style):
        available_table_styles = INSTRUCTIONS['response_formats']['markdown']['table_styles'].keys()
        if style not in available_table_styles:
            raise ValueError(f"Invalid MD_TABLE_STYLE. Available styles: {list(INSTRUCTIONS['table_formatting'].keys())}.")
        self.MD_TABLE_STYLE = INSTRUCTIONS['response_formats']['markdown']['table_styles'][style]
    
    @staticmethod      
    def get_format_styles():
        available_formats = list(INSTRUCTIONS['response_formats'].keys())
        print("Available response formats:", available_formats)
    
    @staticmethod      
    def get_role_contexts():
        available_role_contexts = list(INSTRUCTIONS['role_contexts'].keys())
        print("Available role contexts:", available_role_contexts)

    def get_response(self, user_prompt, format_style='markdown', save_output=False, print_response=False):
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
        
        self.format_style = format_style.lower()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # for output file name
        
        # handler = self.context_handlers.get(self.role_context)
        # if handler is None:
        #     raise ValueError(f"Invalid context: {self.role_context}")
        
        system_role, user_content = self._handle_role_instructions(user_prompt) # change to handler(user_prompt) for context handler process
        
        # Get instructions for selected format
        response_instruct = INSTRUCTIONS['response_formats'][self.format_style]['instruct']
        
        # If selected format is 'markdown' and table style is set, append to response instructions
        # removed: hasattr(self, 'md_table_style') and 
        if self.format_style == 'markdown':
            response_instruct = response_instruct +  \
                INSTRUCTIONS['response_formats']['markdown']['table_styles'][self.MD_TABLE_STYLE]
        
        self.complete_prompt = f"{response_instruct}; {user_content}"
        
        self.response_file = f"{self.role_context}_{timestamp}.{self.file_exts[self.format_style]}"
        
        model = "gpt-3.5-turbo"
        self.response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": self.complete_prompt},
            ],
            temperature=self.temperature,
        )

        # Get the generated text
        self.response_content = self.response['choices'][0]['message']['content']
        
        if self.response_content:
            if save_output:
                with open(self.response_file, 'w') as f:
                    f.write(self.response_content)
            if print_response:
                print(self.response_content)
            return self.response_content
        else:
            print("No response content.")
            return None
        
    def _handle_basic(self, user_prompt):
        system_role = "You're a helpful assistant that answers my questions."
        user_content = user_prompt
        return system_role, user_content

    def _handle_api_explain(self, user_prompt):
        if self.prompt_context:
            prompt_context = INSTRUCTIONS['role_contexts'][self.role_context]['prompt_context_true']
        else:
            prompt_context = INSTRUCTIONS['role_contexts'][self.role_context]['prompt_context_false']
        
        if self.comment_level is not None:
            comment_level = f"Provide {self.comment_level}"
        else:
            comment_level = "Do not add any"
            
        if self.comment_level is not None:
            explain_level = f"Provide {self.explain_level}"
        else:
            explain_level = "Do not give any"
            
        documentation = f"{comment_level} code comments and {explain_level} explanation of the process."
            
        instructions = f"{prompt_context} {INSTRUCTIONS['role_contexts'][self.role_context]['instruct']}"
        user_content = f"{instructions}: {user_prompt}; {documentation}"
        system_role = "You're a helpful expert on analyzing python library documentation."
        return system_role, user_content

    def _handle_code_help(self, user_prompt):
        if self.prompt_context:
            prompt_context = INSTRUCTIONS['role_contexts'][self.role_context]['prompt_context_true']
        else:
            prompt_context = INSTRUCTIONS['role_contexts'][self.role_context]['prompt_context_false']
        
        documentation_instruct = f"Provide {self.comment_level} code comments and {self.explain_level} explanation of the process."
        
        instructions = f"{prompt_context} {INSTRUCTIONS['role_contexts'][self.role_context]['instruct']}"
        user_content = f"{instructions}: {user_prompt}; {documentation_instruct}"
        system_role = "You're a helpful assistant who answers coding language questions."
        return system_role, user_content
    
    def _handle_role_instructions(self, user_prompt):
        if self.role_context != 'basic':
            if self.prompt_context:
                prompt_context = INSTRUCTIONS['role_contexts'][self.role_context]['prompt_context_true']
            else:
                prompt_context = INSTRUCTIONS['role_contexts'][self.role_context]['prompt_context_false']

            comment_level = (
                f"Provide {self.comment_level}" if self.comment_level is not None else "Do not add any"
            )

            explain_level = (
                f"Provide {self.explain_level}" if self.explain_level is not None else "Do not give any"
            )

            default_documentation = f"{comment_level} code comments and {explain_level} explanation of the process."

            documentation = (
                INSTRUCTIONS.get('role_contexts', {})
                            .get(self.role_context, {})
                            .get('documentation', default_documentation)
            )

            instructions = f"{prompt_context} {INSTRUCTIONS['role_contexts'][self.role_context]['instruct']}"
            user_content = f"{instructions}: {user_prompt}; {documentation}"

            system_role = INSTRUCTIONS['role_contexts'][self.role_context]['system_role']
        else:
            system_role = "You're a helpful assistant who answers my questions"
            user_content = user_prompt

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
        # return self.get_response(self.user_prompt)
        
    def show(self):
        if not self.response_content:
            print("No response to show.")
            return
        display_class = self.DISPLAY_MAPPING.get(self.format_style, None)
        if display_class:
            display(display_class(self.response_content))
        else:
            print("Unknown format.")
