import streamlit as st
import os
import random
from web_helpers import generate_response, display_response
import gpt_utils as gpt


# set main page configuration
page_title = "Code Tutor - Learn Code"
# use shortcodes for icons
# see: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)
page_icon = "teacher"
st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    initial_sidebar_state='expanded'
)


# Function to load configurations
# @st.cache_data
def load_app_config():
    config_settings = {
        # main app settings:
        'app_title': config_data['app_ui']['main'].get('title', 'App Title'),
        'title_emoji': config_data['app_ui']['main'].get('title_emoji', 'question'),
        'subheader': config_data['app_ui']['main'].get('subheader', 'How can I help you?'),

        # prompt/box controls:
        'prompt_box': config_data['app_ui']['prompt']['prompt_box'],
        'response_button': config_data['app_ui']['prompt']['response_button'],
        'extra_response_toggle': config_data['app_ui']['prompt']['extra_response_toggle'],
        'allow_null_prompt': config_data['app_ui']['prompt']['allow_null_prompt'],

        # Sidebar Controls
        'api_key': config_data['app_ui']['sidebar']['api_key'],
        'adv_settings': config_data['app_ui']['sidebar']['adv_settings'],
        'role_context': config_data['app_ui']['sidebar']['role_context'],

        'all_role_contexts': config_data['role_contexts']
    }
    return config_settings


# Function to set up the app configurations
# @st.cache_data
def setup_app_config(path_web, path_local):
    if os.path.exists(path_web):
        config_path = path_web
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        config_path = path_local
        api_key = os.environ["OPENAI_API_KEY"]
        
    chat_engine = gpt.ChatEngine(stream=True, api_key=api_key, config_path=config_path)
    config_data = chat_engine.CONFIG
    
    return chat_engine, config_data
  

def extra_response(prompt_1, role_context, response_1):
    with st.spinner('Next lesson...'):
        # get second instruction set for continuing previous conversation
        role_context = config_data['role_contexts'].get(role_context, {})
        default_instruction = 'Provide additional details.'
        instruct_2 = role_context.get('instruct_2', default_instruction)
        prompt_2 = instruct_2
        messages = [prompt_1, response_1, prompt_2]
        return messages


# Function to set up the main UI
def setup_app_controls(app_config):
    st.title(f":{app_config['title_emoji']}: {app_config['app_title']}")
    st.subheader(app_config['subheader'])

    prompt_box = st.empty()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        response_button = st.button(
            f":blue[Get an Answer] :sparkles:",
            help="Generate an answer",
            disabled=not app_config['response_button']  # inverse of enabled status
        )

    with col2:
        extra_response_toggle = st.toggle(
            "Extra Details",
            help="Provide additional, detailed information. Toggle this _before_ getting an answer.",
            key='extra_response',
            value=False,
            disabled=not app_config['extra_response_toggle']
        )

    chat_engine.user_prompt = prompt_box.text_area(
        label="How can I help ?",
        label_visibility="hidden",
        height=185,
        placeholder=app_config['all_role_contexts'][chat_engine.role_context]['prompt_placeholder'],
        key='prompt'
    ) or None
    
    return chat_engine.user_prompt, extra_response_toggle, response_button


# Function to set up the sidebar
def setup_sidebar(chat_engine, app_config):

    api_key = st.sidebar.empty()
    adv_settings = st.sidebar.empty()
    role_context = st.sidebar.empty()

    chat_engine.api_key = api_key.text_input(
        label="OpenAI API Key :key:",
        type="password",
        value=''
    ) or chat_engine.api_key
    
    # Advanced settings expander
    if app_config['adv_settings']:
        adv_settings = adv_settings.expander(
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
            )

    roles = {
        settings.get('display_name', role): role
        for role, settings in config_data['role_contexts'].items()
        if settings.get('enable', False)
    }
    selected_friendly_role = role_context.selectbox('Prompt Context :memo:', roles.keys())
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

    # handle language specific instructions to append to main prompt
    # these additional instructions may eventually be added to the YAML config
    if new_language == 'sql':
        helper_prompt = "If appropriate, use sub-queries, window functions, " \
                        "etc. to make it efficient and concise. Natural language " \
                        + helper_prompt

    return helper_prompt


# Function to handle the response
def handle_response(chat_engine,
                    selected_friendly_role,
                    app_config,
                    extra_response_toggle,
                    helper_prompt='',
                    prompt=None):

    allow_download = not extra_response_toggle
    all_response_content = []

    if prompt is None:
        if app_config['allow_null_prompt']:
            st.info("Not sure what to ask? Creating a random lesson!", icon="🎲")
            sub_keys = list(config_data['random_prompts'].keys())
            random_subkey = random.choice(sub_keys)
            # create prompt with random choice and append keyword for clarity
            prompt = (
                f"'{random.choice(config_data['random_prompts'][random_subkey])}' \
                    {config_data['random_prompts'][random_subkey][0]}"
            )
            chat_engine.role_context = 'random'
        else:
            st.info('Please provide a prompt...', icon='😑')

    try:
        if chat_engine.model == 'gpt-4':
            st.toast('Be patient. Responses from GPT-4 can be slower...', icon="⏳")

        response = generate_response(chat_engine, prompt)

        response_1 = display_response(
            response,
            assistant=allow_download,
            role_name=selected_friendly_role,
            streaming=chat_engine.stream
        )

        if extra_response_toggle:
            chat_engine.stream = False
            prompt_messages = extra_response(prompt, chat_engine.role_context, response_1)
            response_2 = generate_response(chat_engine, prompt_messages)
            display_response(
                response_2,
                assistant=True,
                role_name=selected_friendly_role,
                streaming=chat_engine.stream
            )

        st.toast(':teacher: All replies ready!', icon='✅')

        return response_1

    except Exception as e:
        st.error(f"There was an error handling your question!\n\n{e}", icon='🚨')


# Main function
def main():
    # load appropriate settings based on selected role
    config_settings = load_app_config()

    # save the selected AI context, role name, and any helper prompts
    chat_engine.role_context, selected_friendly_role, helper_prompt = setup_sidebar(chat_engine, config_settings)
    # save the user's prompt, toggle & answer button state
    chat_engine.user_prompt, extra_response_toggle, response_button = setup_app_controls(config_settings)

    # Save currently selected context
    context = chat_engine.role_context
    # Initialize chat history
    if context not in st.session_state:
        st.session_state.setdefault(context, {}).setdefault('messages', [])
    # Display chat history, alternating user prompt and response
    for i, message in enumerate(st.session_state[context]['messages']):
        if i % 2:
            st.chat_message('ai', avatar='👨‍🏫').markdown(message)
        else:
            st.chat_message('user').markdown(message)
    # Initiate the OpenAI response upon button press
    if response_button:
        response = handle_response(chat_engine, selected_friendly_role,
                                   config_settings, extra_response_toggle,
                                   helper_prompt, prompt=chat_engine.user_prompt)
        st.session_state[context]['messages'].extend([chat_engine.user_prompt, response])

    # Store the prompt and the response in a session_state list
    # for use in chatting function
    if chat_prompt := st.chat_input(disabled=not response_button, placeholder="Any questions?"):
        st.session_state[context]['messages'].append(chat_prompt)

        response = handle_response(chat_engine, selected_friendly_role,
                                   config_settings, extra_response_toggle,
                                   prompt=st.session_state[context]['messages'])

        st.session_state[context]['messages'].append(response)


if __name__ == '__main__':
    # create the chat engine instance and retrieve the custom configuration data
    chat_engine, config_data = setup_app_config(
        path_web="/app/code-tutor/web_app/config.yaml",  # streamlit server path
        path_local="config.yaml"  # local path
    )
    main()
