import streamlit as st
import os
import random
import web_helpers as web
import gpt_utils as gpt

# def extra_lesson(prompt_1, role_context, response_1):
#     with st.spinner('Next lesson...'):
#         # get second instruction set for continuing previous conversation
#         role_context = chat_engine.CONFIG['role_contexts'].get(role_context, {})
#         default_instruction = 'Provide additional details.'
#         instruct_2 = role_context.get('instruct_2', default_instruction)
#         prompt_2 = instruct_2
#         messages = [prompt_1, response_1, prompt_2]
#         return messages

# def handle_code_convert(chat_engine.user_prompt, language, language_title):
#     format_style = 'code_convert'
#     header = f"{language_title} translation"
#     chat_engine.user_prompt = f"to {language}: {chat_engine.user_prompt}"
#     return format_style, header, chat_engine.user_prompt

# # Load instructions from JSON file
# path_web = "/app/code-tutor/web_app/config.yaml"  # streamlit server path
# path_local = "config.yaml"

# # Set value for API Key & path for running via local or streamlit
# if os.path.exists(path_web):
#     config_path = path_web
#     api_key=st.secrets["OPENAI_API_KEY"]
# else:
#     config_path = path_local
#     api_key= os.environ['OPENAI_API_KEY']


# # initialize the GPT class
# app = gpt.ChatEngine(config_path=config_path, stream=True, api_key=api_key)

# # get main app title information
# app_title = (
#     chat_engine.CONFIG['app_ui'].get('title', 'App Title')
# )

# title_emoji = (
#     chat_engine.CONFIG['app_ui'].get('title_emoji', 'question')
# )

# page_title = (
#     chat_engine.CONFIG['app_ui'].get('page_title', 'Streamlit App')
# )

# # set page configuration
# st.set_page_config(page_title=page_title, page_icon=title_emoji)

# # BEGIN WIDGETS
# # Side bar controls


# # Open API Key
# chat_engine.api_key = st.sidebar.text_input(
#     label="OpenAI API Key :key:",
#     type="password",
#     help="Get your API key from https://openai.com/"
# ) or chat_engine.api_key

# # Advanced settings expander
# adv_settings = st.sidebar.expander(
#     label="Advanced Settings :gear:",
#     expanded=False
# )

# # Add Open API key and Advanced Settings widgets to the expander
# with adv_settings:
#     chat_engine.model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], help="Account must be authorized for gpt-4")
#     chat_engine.temperature = st.slider(
#         "Temperature", 0.0, 2.0, 0.2, 0.1
#     )
#     chat_engine.temperature = round(chat_engine.temperature * 10) / 10

# convert_languages = chat_engine.CONFIG['role_contexts']['code_convert']['languages']
# convert_file_formats = chat_engine.CONFIG['role_contexts']['code_convert']['file_formats']
# convert_options = convert_languages + convert_file_formats

# #### Sidebar with dropdown of friendly role names ###

# # Get all list roles
# json_roles = chat_engine.get_role_contexts()

# # Create dictionary of enabled roles and display names
# # default to role key if no display_name value set
# roles = {
#     settings.get('display_name', role): role
#     for role, settings in chat_engine.CONFIG['role_contexts'].items()
#     if settings.get('enable', False)
# }

# selected_friendly_role = st.sidebar.selectbox(
#     'Prompt Context :memo:',
#     roles.keys()
# )

# # get the role context name from json
# selected_json_role = roles[selected_friendly_role]
# # set the class variable to json name
# chat_engine.role_context = selected_json_role
# # get the button phrase based on selected role
# button_phrase = (
#     chat_engine.CONFIG['role_contexts'][selected_json_role].get('button_phrase', 'Enter')
# )

# # get other app title information
# subheader = (
#     chat_engine.CONFIG['app_ui'].get('subheader', 'How can I help you?')
# )

# # configure app title information
# st.title(f":{title_emoji}: {app_title}")
# st.subheader(subheader)
# prompt_box = st.empty()

# # Create two columns
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     answer_button = st.button(
#         f":blue[{button_phrase}] :sparkles:",
#         help="Generate an answer"
#     )
# with col2:
#     extra_lesson_toggle = st.toggle(
#         "Extra Details",
#         help="Provide additional, detailed information. Toggle this _before_ getting an answer.",
#         key='extra_lesson',
#         value=False
#     )

# prompt_placeholder = (
#     chat_engine.CONFIG['role_contexts'][selected_json_role].get('prompt_placeholder', 'Enter your prompt...')
# )

# chat_engine.user_prompt = prompt_box.text_area(
#     label="How can I help ?",
#     label_visibility="hidden",
#     height=185,
#     placeholder=prompt_placeholder,
#     key='prompt'
# ) or None






# Function to load configurations
def load_config_settings(chat_engine, selected_role):
    config_settings = {
        # general app settings:
        'app_title': CONFIG['app_ui'].get('title', 'App Title'),
        'title_emoji': CONFIG['app_ui'].get('title_emoji', 'question'),
        'page_title': CONFIG['app_ui'].get('page_title', 'Streamlit App'),
        'subheader': CONFIG['app_ui'].get('subheader', 'How can I help you?'),
        # role specific:
        'button_phrase': CONFIG['role_contexts'][selected_role].get('button_phrase', 'Enter'),
        'prompt_placeholder': CONFIG['role_contexts'][selected_role].get('prompt_placeholder', 'Enter your prompt...')
    }
    return config_settings

# Function to setup the app configurations
def setup_app_config():
    path_web = "/app/code-tutor/web_app/config.yaml"  # streamlit server path
    path_local = "config.yaml"
    if os.path.exists(path_web):
        config_path = path_web
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        config_path = path_local
        api_key = os.environ['OPENAI_API_KEY']
    return config_path, api_key
  
def extra_lesson(prompt_1, role_context, response_1):
    with st.spinner('Next lesson...'):
        # get second instruction set for continuing previous conversation
        role_context = CONFIG['role_contexts'].get(role_context, {})
        default_instruction = 'Provide additional details.'
        instruct_2 = role_context.get('instruct_2', default_instruction)
        prompt_2 = instruct_2
        messages = [prompt_1, response_1, prompt_2]
        return messages

# Function to setup the main UI
def setup_main_area(config_settings):
    st.title(f":{config_settings['title_emoji']}: {config_settings['app_title']}")
    st.subheader(config_settings['subheader'])
    prompt_box = st.empty()
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        answer_button = st.button(
            f":blue[{config_settings['button_phrase']}] :sparkles:",
            help="Generate an answer"
        )
    with col2:
        extra_lesson_toggle = st.toggle(
            "Extra Details",
            help="Provide additional, detailed information. Toggle this _before_ getting an answer.",
            key='extra_lesson',
            value=False
        )

    chat_engine.user_prompt = prompt_box.text_area(
        label="How can I help ?",
        label_visibility="hidden",
        height=185,
        placeholder=config_settings['prompt_placeholder'],
        key='prompt'
    ) or None
    
    return chat_engine.user_prompt, extra_lesson_toggle, answer_button


# Function to setup the sidebar
def setup_sidebar(chat_engine):
    
    chat_engine.api_key = st.sidebar.text_input(
        "OpenAI API Key :key:", type="password"
    ) or chat_engine.api_key
    
    # Advanced settings expander
    adv_settings = st.sidebar.expander(
        label="Advanced Settings :gear:",
        expanded=False
    )

    # Add Open API key and Advanced Settings widgets to the expander
    with adv_settings:
        chat_engine.model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], help="Account must be authorized for gpt-4")
        chat_engine.temperature = st.slider(
            "Temperature", 0.0, 2.0, 0.2, 0.1
        )
        chat_engine.temperature = round(chat_engine.temperature * 10) / 10
    
    roles = {
        settings.get('display_name', role): role
        for role, settings in CONFIG['role_contexts'].items()
        if settings.get('enable', False)
    }
    selected_friendly_role = st.sidebar.selectbox('Prompt Context :memo:', roles.keys())
    selected_role = roles[selected_friendly_role]

    if selected_role == 'code_convert':
        handle_code_convert()
                
    return selected_role, selected_friendly_role

# Function to handle code_convert settings
def handle_code_convert():
    convert_settings = {
        'languages': CONFIG['role_contexts']['code_convert'].get('languages', []),
        'file_formats': CONFIG['role_contexts']['code_convert'].get('file_formats', []),
    }
    convert_options = convert_settings['languages'] + convert_settings['file_formats']
    selected_language = st.sidebar.selectbox(
            "Convert to:", 
            convert_options,
            key='language',
            format_func=lambda x: f"{x} (file format)" if x in convert_settings['file_formats'] else x
        )
    new_language = selected_language.lower().replace('-', '')
    chat_engine.user_prompt = f"to {new_language}: {chat_engine.user_prompt}"
    
    return new_language

# Function to handle the response
def handle_response(chat_engine, extra_lesson_toggle, selected_friendly_role):
    try:
        allow_download = not extra_lesson_toggle
        all_response_content = []

        if chat_engine.model == 'gpt-4':
            st.toast('Be patient. Responses from GPT-4 can be slower ...', icon="⏳")

        if chat_engine.user_prompt is None:
            if CONFIG['allow_null_prompt']:
                st.info("Not sure what to ask? Creating a random lesson!", icon="🎲")
                subkeys = list(CONFIG['random_prompts'].keys())
                random_subkey = random.choice(subkeys)
                chat_engine.user_prompt = random.choice(CONFIG['random_prompts'][random_subkey])
                chat_engine.role_context = 'random'
            else:
                st.info('Please provide a prompt...', icon='😑')

        response = web.generate_response(chat_engine, chat_engine.user_prompt)
        
        displayed_response = web.display_response(
            response,
            assistant=allow_download,
            all_response_content=all_response_content,
            role_name=selected_friendly_role,
            streaming=chat_engine.stream
        )
        
        chat_engine.complete_prompt
        

        if extra_lesson_toggle:
            chat_engine.stream = False
            prompt_messages = extra_lesson(chat_engine.user_prompt, chat_engine.role_context, displayed_response)
            extra_response = web.generate_response(chat_engine, prompt_messages)
            web.display_response(
                extra_response,
                assistant=True,
                all_response_content=all_response_content,
                role_name=selected_friendly_role,
                streaming=chat_engine.stream
            )

        st.toast(':teacher: All replies complete!', icon='✅')

    except Exception as e:
        st.error(f"There was an error while the response was being generated. {e}", icon='🚨')

# Main function
def main():
    selected_role, selected_friendly_role = setup_sidebar(chat_engine)
    
    config_settings = load_config_settings(chat_engine, selected_role)

    chat_engine.user_prompt, extra_lesson_toggle, answer_button = setup_main_area(config_settings)

    if answer_button:
        handle_response(chat_engine, extra_lesson_toggle, selected_friendly_role)

if __name__ == '__main__':
    
    config_path, api_key = setup_app_config()
    chat_engine = gpt.ChatEngine(config_path=config_path, stream=True, api_key=api_key)
    
    CONFIG = chat_engine.CONFIG
    
    main()