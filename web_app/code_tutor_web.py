import streamlit as st
import os
import random
from web_helpers import generate_response, display_response
import gpt_utils as gpt


# set main page configuration
page_title = "Code Tutor - Learn Code"
page_icon = "teacher"
st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    initial_sidebar_state='expanded'
)


# Function to load configurations
def load_app_config(selected_role):
    config_settings = {
        # general app settings:
        'app_title': config_data['app_ui'].get('title', 'App Title'),
        'title_emoji': config_data['app_ui'].get('title_emoji', 'question'),
        'subheader': config_data['app_ui'].get('subheader', 'How can I help you?'),
        # role specific:
        'button_phrase': config_data['role_contexts'][selected_role].get('button_phrase', 'Enter'),
        'prompt_placeholder': config_data['role_contexts'][selected_role].get('prompt_placeholder',
                                                                              'Enter your prompt...')
    }
    return config_settings


# Function to set up the app configurations
@st.cache_data
def setup_app_config(path_web, path_local):
    if os.path.exists(path_web):
        config_path = path_web
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        config_path = path_local
        api_key = os.environ["OPENAI_API_KEY"]
        
    chat_engine = gpt.ChatEngine(config_path=config_path, stream=True, api_key=api_key)
    config_data = chat_engine.CONFIG
    
    return chat_engine, config_data
  

def extra_lesson(prompt_1, role_context, response_1):
    with st.spinner('Next lesson...'):
        # get second instruction set for continuing previous conversation
        role_context = config_data['role_contexts'].get(role_context, {})
        default_instruction = 'Provide additional details.'
        instruct_2 = role_context.get('instruct_2', default_instruction)
        prompt_2 = instruct_2
        messages = [prompt_1, response_1, prompt_2]
        return messages


# Function to set up the main UI
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


# Function to set up the sidebar
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
        chat_engine.model = st.selectbox(
            "Model", 
            ["gpt-3.5-turbo", "gpt-4"],
            index=1,  # MOST RECENT CHANGE
            help="Some API keys are not authorized for use with gpt-4"
        )
        chat_engine.temperature = st.slider(
            "Temperature", 0.0, 2.0, 1.0, 0.1,
            help="""
            temperature controls the "creativity" of the response.
            A higher value results in more diverse and unexpected 
            responses, while lower values result in more conservative
            and predictable responses.
            """
        )  # MOST RECENT CHANGE (removed rounding)
            
    roles = {
        settings.get('display_name', role): role
        for role, settings in config_data['role_contexts'].items()
        if settings.get('enable', False)
    }
    selected_friendly_role = st.sidebar.selectbox('Prompt Context :memo:', roles.keys())
    selected_role = roles[selected_friendly_role]

    helper_prompt = ''

    # adjust prompt or other parameters based on selected role context
    if selected_role == 'code_convert':
        helper_prompt = handle_code_convert()
                
    return selected_role, selected_friendly_role, helper_prompt


# Function to handle code_convert settings
def handle_code_convert():
    convert_settings = {
        'languages': config_data['role_contexts']['code_convert'].get('languages', []),
        'file_formats': config_data['role_contexts']['code_convert'].get('file_formats', []),
    }
    convert_options = convert_settings['languages'] + convert_settings['file_formats']
    selected_language = st.sidebar.selectbox(
            "Convert to:", 
            convert_options,
            key='language',
            format_func=lambda x: f"{x} (file format)" if x in convert_settings['file_formats'] else x
        )
    new_language = selected_language.lower().replace('-', '')
    helper_prompt = f"to {new_language}: "
    
    return helper_prompt


# Function to handle the response
def handle_response(chat_engine, extra_lesson_toggle, selected_friendly_role, helper_prompt):
    try:
        allow_download = not extra_lesson_toggle
        all_response_content = []

        if chat_engine.model == 'gpt-4':
            st.toast('Be patient. Responses from GPT-4 can be slower...', icon="⏳")

        if chat_engine.user_prompt is None:
            if config_data['allow_null_prompt']:
                st.info("Not sure what to ask? Creating a random lesson!", icon="🎲")
                subkeys = list(config_data['random_prompts'].keys())
                random_subkey = random.choice(subkeys)
                # create prompt with random choice and append keyword for clarity
                chat_engine.user_prompt = (
                    f"'{random.choice(config_data['random_prompts'][random_subkey])}' \
                        {config_data['random_prompts'][random_subkey][0]}"
                )
                chat_engine.role_context = 'random'
            else:
                st.info('Please provide a prompt...', icon='😑')
        else:
            chat_engine.user_prompt = f"{helper_prompt}{chat_engine.user_prompt}"

        response = generate_response(chat_engsine, chat_engine.user_prompt)

        displayed_response = display_response(
            response,
            assistant=allow_download,
            all_response_content=all_response_content,
            role_name=selected_friendly_role,
            streaming=chat_engine.stream
        )

        if extra_lesson_toggle:
            chat_engine.stream = False
            prompt_messages = extra_lesson(chat_engine.user_prompt, chat_engine.role_context, displayed_response)
            extra_response = generate_response(chat_engine, prompt_messages)
            display_response(
                extra_response,
                assistant=True,
                all_response_content=all_response_content,
                role_name=selected_friendly_role,
                streaming=chat_engine.stream
            )

        st.toast(':teacher: All replies ready!', icon='✅')

    except Exception as e:
        st.error(f"There was an error while your request was being sent: {e}", icon='🚨')


# Main function
def main():
    # save the selected AI context, role name, and any helper prompts
    chat_engine.role_context, selected_friendly_role, helper_prompt = setup_sidebar(chat_engine)
    # load appropriate settings based on selected role
    config_settings = load_app_config(chat_engine.role_context)
    # save the user's prompt, toggle & answer button state
    chat_engine.user_prompt, extra_lesson_toggle, answer_button = setup_main_area(config_settings)
    # if answer button is clicked, initiate the OpenAI response
    if answer_button:
        handle_response(chat_engine, extra_lesson_toggle, selected_friendly_role, helper_prompt)


if __name__ == '__main__':
    # create the chat engine instance and retrieve the custom configuration data
    chat_engine, config_data = setup_app_config(
        path_web="/app/code-tutor/web_app/config.yaml",  # streamlit server path
        path_local="config.yaml"  # local path
    )
    main()
