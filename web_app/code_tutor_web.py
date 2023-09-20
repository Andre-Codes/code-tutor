# import gpt_service_web as gpt
import streamlit as st
import os
import openai
import json
import datetime
import re

# Load instructions from JSON file
with open("instructions_web.json", "r") as f:
    INSTRUCTIONS = json.load(f)

class CodeTutor:
    """
    A class for interacting with GPT models via the OpenAI API.
    
    Attributes:
        api_key (str): The OpenAI API key, sourced from environment variables.
        model (str): The GPT model name to be used. Defaults to "gpt-3.5-turbo".
        role_context (str): Operational context for the GPT model, e.g., 'basic', 'api_explain'.
        prompt_context (bool): Whether additional context will be provided in the prompt. 
        comment_level (str): Level of comment verbosity.
        explain_level (str): Level of explanation verbosity.
        temperature (float): Controls randomness in output. Lower is more deterministic.
        
    Class Variables:
        DISPLAY_MAPPING (dict): Mappings for IPython.display function names.
        MD_TABLE_STYLE (str): Default style for Markdown tables.
        
    Methods:
        __init__(): Initializes class attributes.
        set_md_table_style(): Sets Markdown table style.
        get_format_styles(): Prints available response formats.
        get_role_contexts(): Prints available role contexts.
        _validate_and_assign_params(): Validates and assigns prompt and format_style.
        _build_prompt(): Constructs the complete prompt for OpenAI API call.
        _make_openai_call(): Makes the API call and stores the response.
        _handle_output(): Handles saving and displaying the response.
        get_response(): Main function to get a response from the GPT model.
        _handle_role_instructions(): Constructs role-specific instructions for the prompt.
        show(): Displays the generated content.
    """
    
    # Class variables
    # DISPLAY_MAPPING = { # mappings for IPython.display function names
    #     'html': HTML,
    #     'markdown': Markdown
    # }
    
    MD_TABLE_STYLE = "pipes" # default format for markdown tables
    
    def __init__(
        self, 
        role_context=None,
        prompt_context=False,
        comment_level=None,
        explain_level=None,
        temperature=None,
        model="gpt-3.5-turbo",
        api_key=os.environ['OPENAI_API_KEY']):
        """
        Initializes the GPTService class with settings to control the prompt and response.

        # Parameters
        ----------
            role_context (str, optional): Operational context for GPT. This directly control \
                what is sent to the GPT model in addition to the user inputted prompt. \
                    Use the `get_role_contexts()` method to view the available roles. \
                        Defaults to 'basic'.
            prompt_context (bool, optional): Whether additional context will be provided; \
                typically as API documentation or code. Defaults to False.
            comment_level (str, optional): Level of comment verbosity. Defaults to 'normal'.
            explain_level (str, optional): Level of explanation verbosity. Defaults to 'concise'.
            temperature (float, optional): Controls randomness in output. Defaults to 0.
            model (str, optional): The GPT model name to use. Defaults to "gpt-3.5-turbo".
        """
        
        # Set up API access
        self.api_key = api_key
                
        # Set the GPT model
        self.model = model
        
        # Validate and set role_context
        available_role_contexts = INSTRUCTIONS.get('role_contexts', {}).keys()
        self.role_context = role_context if role_context in available_role_contexts else 'basic'
        
        # Validate and set prompt_context
        if not isinstance(prompt_context, bool):
            raise ValueError("prompt_context must be a boolean value: True or False")
        self.prompt_context = prompt_context
        
        # Validate and set comment_level
        comment_levels = INSTRUCTIONS['comment_levels']
        self.comment_level = comment_level if comment_level in comment_levels \
            or comment_level is None else 'normal'
        
        # Validate and set explain_level
        explain_levels = INSTRUCTIONS['explain_levels']
        self.explain_level = explain_level if explain_level in explain_levels \
            or explain_level is None else 'concise'
        
        # Validate and set temperature
        self.temperature = temperature

    
    def set_md_table_style(self, style):
        available_table_styles = INSTRUCTIONS['response_formats']['markdown']['table_styles'].keys()
        if style not in available_table_styles:
            raise ValueError(f"Invalid MD_TABLE_STYLE. Available styles: {list(INSTRUCTIONS['table_formatting'].keys())}.")
        self.MD_TABLE_STYLE = INSTRUCTIONS['response_formats']['markdown']['table_styles'][style]
        
    def get_format_styles():
        available_formats = list(INSTRUCTIONS['response_formats'].keys())
        print("Available response formats:", available_formats)
         
    def get_role_contexts():
        available_role_contexts = list(INSTRUCTIONS['role_contexts'].keys())
        return available_role_contexts

    def _validate_and_assign_params(self, prompt, format_style):
        if prompt is None:
            raise ValueError("Prompt can't be None.")
        self.prompt = prompt
        self.format_style = format_style.lower()

    def _build_prompt(self):
        self.system_role, user_content = self._handle_role_instructions(self.prompt)

        response_instruct = INSTRUCTIONS['response_formats'][self.format_style]['instruct']
        if self.format_style == 'markdown':
            response_instruct += INSTRUCTIONS['response_formats']['markdown']['table_styles'][self.MD_TABLE_STYLE]
        elif self.format_style == 'html':
            response_instruct += INSTRUCTIONS['response_formats']['html']['css']

        self.complete_prompt = f"{response_instruct}; {user_content}"

    def _make_openai_call(self):
        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.__messages,
                temperature=self.temperature,
            )
        except Exception as e:
            return "Connection to API failed - Verify internet connection or API key"
        if response:
            self.response_content = response['choices'][0]['message']['content']

    def _handle_output(self, save_output, print_raw, **kwargs):
        only_code = kwargs.get('only_code', False)
        
        file_exts = {
            "markdown": "md",
            "html": "html"
        }
        
        try:
            if self.response_content:
                if save_output:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # for output file name
                    response_file = f"{self.role_context}_{timestamp}.{file_exts[self.format_style]}"
                    with open(response_file, 'w') as f:
                        f.write(self.response_content)
                if print_raw:
                    print(self.response_content)
                content = self.show(content=self.response_content, only_code=only_code)
                return content
            else:
                return "No response."
        except Exception as e:
            return "***Your request could not be completed - Verify internet connection and/or API key***"
            
    def _build_messages(self, prompt):
        # Validate that all items in 'prompt' are strings
        if not all(isinstance(item, str) for item in prompt):
            raise ValueError("All elements in the list should be strings")
        
        # Initialize system message
        system_msg = [{"role": "system", "content": self.system_role}]
        
        # Determine user and assistant messages based on the length of the 'prompt'
        if len(prompt) > 1:
            user_assistant_msgs = [
                {
                    "role": "assistant" if i % 2 == 0 else "user", 
                    "content": prompt[i]
                }
                for i in range(len(prompt))
            ]
        else:
            user_assistant_msgs = [{"role": "user", "content": self.complete_prompt}]
        
        # Combine system, user, and assistant messages
        self.__messages = system_msg + user_assistant_msgs

    def get_response(
            self,
            prompt=None,
            format_style='markdown',
            save_output=False,
            print_raw=False,
            **kwargs
        ):
        # _build_messages requires prompt to be a list
        # convert prompt to a list if it is not already
        prompt = [prompt] if not isinstance(prompt, list) else prompt
        self._validate_and_assign_params(prompt, format_style)
        self._build_prompt()
        self._build_messages(prompt)
        self._make_openai_call()
        content = self._handle_output(save_output, print_raw, **kwargs)
        # Return finished response from OpenAI
        return content
    
    def _handle_role_instructions(self, user_prompt):
        if self.role_context != 'basic':
            prompt_context_key = 'prompt_context_true' if self.prompt_context else 'prompt_context_false'
            prompt_context = INSTRUCTIONS['role_contexts'][self.role_context][prompt_context_key]

            comment_level = f"Provide {self.comment_level}" if self.comment_level is not None else "Do not add any"
            explain_level = f"Provide {self.explain_level}" if self.explain_level is not None else "Do not give any"
            default_documentation = (
                f"{comment_level} code comments and {explain_level} explanation of the process."
            )

            documentation = (
                INSTRUCTIONS.get('role_contexts', {})
                            .get(self.role_context, {})
                            .get('documentation', default_documentation)
            )

            instructions = (
                f"{prompt_context} {INSTRUCTIONS['role_contexts'][self.role_context]['instruct']}"
            )
            user_content = f"{instructions}: {user_prompt}; {documentation}"

            system_role = INSTRUCTIONS['role_contexts'][self.role_context]['system_role']
        else:
            system_role = "You're a helpful assistant who answers my questions"
            user_content = user_prompt

        return system_role, user_content
        
    def show(self, content=None, only_code=False):
        if not self.response_content:
            print("No response to show.")
            return
            
        # display_class = self.DISPLAY_MAPPING.get(self.format_style, None)
        
        if not content:
            content = self.response_content
        
        if only_code:
            pattern = r'(```.*?```)'
            matches = re.findall(pattern, content, re.DOTALL) 
            content = '\n'.join(matches)
            
        return content


st.set_page_config(page_title="👨‍🏫 Code Tutor - Learn Code")

# initalize the class with role context
ct = CodeTutor(
    role_context = "code_help", 
    explain_level = 'concise', 
    comment_level = 'normal'
)

def generate_response(prompt, only_code):
    with st.spinner('Forming an answer... :thought_balloon:'):
        return ct.get_response(
            prompt = prompt, 
            only_code = only_code, 
            format_style = format_style
        )

def display_content(content, custom_header=None):
    # st.text(ct.response_content)
    # st.text(ct.complete_prompt)
    st.divider()
    with st.container():
        if custom_header:
            st.markdown(f"{custom_header}")
        if content[:3] == "***":
            st.warning(content)
        else:
            st.markdown(content)

def extra_lesson(user_prompt, role_context):
    with st.spinner('Next lesson...'):
        prompt2 = INSTRUCTIONS['role_contexts'][role_context]['instruct_2']
        messages = [user_prompt, ct.response_content, prompt2]
        return ct.get_response(prompt=messages)

def handle_code_convert(user_prompt, language):
    format_style = 'code_convert'
    header = f"# {language} Translation"
    user_prompt = f"to {language}: {user_prompt}"
    return format_style, header, user_prompt

# BEGIN WIDGETS
# Side bar controls
# Open API Key
ct.api_key = st.sidebar.text_input(
    label = "Open API Key :key:", 
    type = "password",
    help = "Get your API key from https://openai.com/"
) or ct.api_key

# Advanced settings expander
adv_settings = st.sidebar.expander(
    label = "Advanced Settings :gear:", 
    expanded = False
)

# Add Open API key and Advanced Settings widgets to the expander
with adv_settings:
    ct.model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], help="Account must be authorized for gpt-4")
    ct.temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.2, 0.1
    )
    ct.temperature = round(ct.temperature * 10) / 10

convert_languages = INSTRUCTIONS['role_contexts']['code_convert']['languages']
convert_file_formats = INSTRUCTIONS['role_contexts']['code_convert']['file_formats']
convert_options = convert_languages + convert_file_formats

custom_header = None

# Sidebar with dropdown
roles = CodeTutor.get_role_contexts()
roles = {INSTRUCTIONS['role_contexts'][role]['display_name']: role for role in roles}

selected_friendly_role = st.sidebar.selectbox(
    'Lesson Context :memo:', 
    roles.keys()
)

# get the role context name from json
selected_json_role = roles[selected_friendly_role]
# set the class variable to json name
ct.role_context = selected_json_role
# get the button phrase based on selected role
button_phrase = (
    INSTRUCTIONS['role_contexts'][selected_json_role]['button_phrase']
)

st.title(":teacher: Code Tutor")

prompt_box = st.empty()

# Create two columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    answer_button = st.button(
        f":blue[{button_phrase}] :sparkles:", 
        help="Generate an answer"
    )
with col2:
    just_code_toggle = st.toggle(
        "Just code", 
        help="The result will contain only code. This is enforced when selecting 'Convert Code'.", 
        key='just_code'
    )
with col3:
    extra_lesson_toggle = st.toggle(
        "Extra lesson", 
        help="Provide additional information to the related question. The selected AI role directly affects this."
    )

user_prompt = prompt_box.text_area(
    label="How can I help?",
    height=185,
    placeholder=INSTRUCTIONS['role_contexts'][selected_json_role]['prompt_placeholder'], 
    key='prompt'
)

if selected_json_role == 'code_convert':
    # Display selection box for languages to convert to
    selected_language = st.sidebar.selectbox(
    "Convert to:", convert_options, format_func=lambda x: f"{x} (file format)" if x in convert_file_formats else x
    )
    convert_language = selected_language.lower().replace('-', '')
    format_style, custom_header, user_prompt = handle_code_convert(user_prompt, convert_language)
else:
    format_style = 'markdown'

# 
if answer_button:
    content = generate_response(user_prompt, just_code_toggle)
    display_content(content, custom_header=custom_header)
    
    if extra_lesson_toggle:
        more_content = extra_lesson(user_prompt, ct.role_context)
        display_content(more_content, custom_header="Further Explanation")
