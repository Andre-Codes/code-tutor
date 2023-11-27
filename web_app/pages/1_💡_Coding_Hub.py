import streamlit as st
import os
import random
from pathlib import Path
from pages.utils.web_helpers import generate_response, display_response
import pages.utils.gpt_utils as gpt

# set main page configuration
page_title = "Learning Lab"
# use shortcodes for icons
# see: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)
page_icon = ":bulb:"
st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    initial_sidebar_state='expanded'
)


# Function to load configurations
@st.cache_data
def load_app_config():
    config_settings = {
        # main app settings:
        'app_title': config_data['app_ui']['main'].get('title', 'App Title'),
        'title_emoji': config_data['app_ui']['main'].get('title_emoji', 'question'),
        'subheader': config_data['app_ui']['main'].get('subheader', 'How can I help you?'),

        # prompt/box controls:
        'prompt_box': config_data['app_ui']['prompt']['prompt_box'],
        'response_button': config_data['app_ui']['prompt']['response_button'],
        'allow_null_prompt': config_data['app_ui']['prompt']['allow_null_prompt'],

        # Sidebar Controls
        'api_key': config_data['app_ui']['sidebar']['api_key'],
        'adv_settings': config_data['app_ui']['sidebar']['adv_settings'],
        'role_context': config_data['app_ui']['sidebar']['role_context'],

        'all_role_contexts': config_data['role_contexts']
    }
    return config_settings


# Function to set up the app configurations
@st.cache_data
def setup_app_config(base_path_web, base_path_local, config_file, logo_name, avatar_name):
    # Convert string paths to Path objects
    base_path_web = Path(base_path_web)
    base_path_local = Path(base_path_local)
    # Determine the base path depending on what exists
    base_path = base_path_web if base_path_web.exists() else base_path_local
    # Set up file paths uniformly
    config_file_path = base_path / config_file
    logo_path = base_path / logo_name
    avatar_path = base_path / avatar_name
    # Get the API key based on the base path
    api_key = st.secrets["OPENAI_API_KEY"] if base_path == base_path_web else os.environ["OPENAI_API_KEY"]
    # Instantiate the ChatEngine with the config file path as a string
    chat_engine = gpt.ChatEngine(stream=False, api_key=api_key, config_path=str(config_file_path))
    # Grab the config data from the engine
    config_data = chat_engine.CONFIG
    return chat_engine, config_data, str(logo_path), str(avatar_path)


# Function to set up the main UI
def setup_app_controls(app_config):
    st.title(f":{app_config['title_emoji']}: :blue[{app_config['app_title']}]")
    st.subheader(app_config['subheader'])

    prompt_box = st.empty()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        response_button = st.button(
            f":blue[Ask Code Tutor!] :sparkles:",
            help="Get an answer",
            disabled=not app_config['response_button']  # inverse of enabled status
        )

    chat_engine.user_prompt = prompt_box.text_area(
        label="Enter a prompt",
        label_visibility="visible",
        height=185,
        placeholder=app_config['all_role_contexts'][chat_engine.role_context]['prompt_placeholder'],
        key='prompt',
        help="""
        Entering in a prompt/question here will always start a new lesson 
        context. After conversing with Code Tutor, you can return here at 
        any time to start a new lesson without removing any previous ones.
        This allows you to create a long thread of multiple lesson contexts,
        as well as compare different model and temp. values as you progress.
        """
    ) or None

    return chat_engine.user_prompt, response_button


# Function to set up the sidebar
def setup_sidebar(chat_engine, app_config):
    logo = st.sidebar.empty()
    api_key = st.sidebar.empty()
    adv_settings = st.sidebar.empty()
    role_context = st.sidebar.empty()
    logo.image(page_logo)

    llm_models_dict = {
        "GPT-3": "gpt-3.5-turbo",
        "GPT-4": "gpt-4",
        "GPT-4 Turbo": "gpt-4-1106-preview"
    }

    chat_engine.api_key = api_key.text_input(
        label="OpenAI API Key :key:",
        type="password",
        value='',
        help="Entering your own key is optional. This app is completely free to use until rate limits are exceeded."
    ) or chat_engine.api_key

    # Advanced settings expander
    if app_config['adv_settings']:
        adv_settings = adv_settings.expander(
            label="Advanced Settings :gear:",
            expanded=False
        )

        # Add Open API key and Advanced Settings widgets to the expander
        with adv_settings:
            llm_model = st.selectbox(
                "Model",
                ["GPT-3", "GPT-4", "GPT-4 Turbo"],
                index=2,
                help="""
                - **GPT-3**: fast and streamlined responses, prone to mistakes.
                - **GPT-4**: slower response, better accuracy and attention 
                 to detail. 
                 - **GPT-4 Turbo**: fastest, most advanced v4 model.
                 """
            )

            chat_engine.model = llm_models_dict[llm_model]

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

    # perform actions based on selected role context
    if selected_role == 'code_convert':
        if llm_model == "GPT-3":
            warning_msg = """
            The 'GPT-4' models are **mandatory** for code conversion. If the 
            selected model is GPT-3, it will be overriden upon submitting the prompt.
            """
            st.sidebar.warning(warning_msg, icon="⚠️")
            chat_engine.model = "gpt-4-1106-preview"
        # Save code_convert system role and pass to handling function
        system_role = config_data['role_contexts']['code_convert']['system_role']
        handle_code_convert(system_role)

    st.sidebar.divider()
    disclaimer = st.sidebar.container()
    disclaimer.info("""
    The content provided on this platform is generated using 
    artificial intelligence (AI) techniques. AI-generated 
    content is subject to potential errors, biases, and inaccuracies inherent 
    to automated systems. Users are advised to exercise discretion and 
    critically evaluate the content before relying on it for decision-making, 
    coding, or any other purpose. Official OpenAI terms and policies can be
    read here: https://openai.com/policies
    """, icon="ℹ️")

    return selected_role, selected_friendly_role


# Function to handle code_convert settings
def handle_code_convert(system_role):
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

    # handle language specific instructions to append to main prompt
    # these additional instructions may eventually be added to the YAML config
    if new_language == 'sql':
        chat_engine.system_role = system_role.format(
            f"{new_language} from natural language. If appropriate, use sub-queries, window "
            f"functions, with statements, pivot tables, etc. to make it efficient and concise"
        )
    else:
        chat_engine.system_role = system_role.format(new_language)


# Function to handle the response
def handle_response(chat_engine,
                    context,
                    app_config,
                    prompt=None):

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
        response = generate_response(chat_engine, prompt, chat_engine.role_context)

        response_1 = display_response(
            response,
            download=True,
            role_name=context,
            streaming=chat_engine.stream
        )

        st.toast(':teacher: Done!', icon='✅')

        return response_1, prompt

    except Exception as e:
        raise e


# Main function
def main():
    # load appropriate settings based on selected role
    config_settings = load_app_config()

    # save the selected AI context, role name
    chat_engine.role_context, selected_friendly_role = setup_sidebar(chat_engine, config_settings)
    # save the user's prompt, toggle & answer button state
    chat_engine.user_prompt, response_button = setup_app_controls(config_settings)

    # Save currently selected context
    context = chat_engine.role_context
    # Initialize chat history
    if context not in st.session_state:
        st.session_state.setdefault(context, {}).setdefault('messages', [])

    # Display chat history, alternating user prompt and response
    for i, message in enumerate(st.session_state[context]['messages']):
        if i % 2:
            st.chat_message('ai', avatar=ai_avatar).markdown(message)
        else:
            st.chat_message('user').text(message)
    # Initiate the OpenAI response upon button press
    if response_button:
        try:
            response, prompt = handle_response(chat_engine, context,
                                               config_settings, prompt=chat_engine.user_prompt)
            st.session_state[context]['messages'].append(prompt)
            st.session_state[context]['messages'].append(response)
        except Exception as e:
            error_message = str(e)
            error_dict_str = error_message.split(' - ')[1]
            error_dict = eval(error_dict_str)
            error_message = error_dict['error']['message']
            if error_dict['error']['code'] in ('billing_hard_limit_reached', 'insufficient_quota'):
                st.error(icon='😪',
                         body=f"""**No more requests allowed**. 
                    \n\n If you are using your own API 🔑 key, increase ⏫ your billing limit.
                    Otherwise, try again later... (our wallets are tired)
                """)
            else:
                st.error(f"There was an error handling your question!\n\n{error_message}", icon='🚨')

    # Store the prompt and the response in a session_state list
    # for use in chatting function
    if len(st.session_state[context]['messages']) > 1:
        if chat_prompt := st.chat_input(placeholder="Any questions?"):
            st.chat_message('user').markdown(chat_prompt)
            st.session_state[context]['messages'].append(chat_prompt)

            response, _ = handle_response(chat_engine, selected_friendly_role,
                                          config_settings, prompt=st.session_state[context]['messages'])

            st.session_state[context]['messages'].append(response)


if __name__ == '__main__':
    # create the chat engine instance and retrieve the custom configuration data
    chat_engine, config_data, page_logo, ai_avatar = setup_app_config(
        base_path_web="/mount/src/code-tutor/web_app/pages/",  # streamlit server path
        base_path_local="pages/",  # local path
        config_file="utils/1_config.yaml",
        logo_name="images/ct_logo_head.png",
        avatar_name="images/ct_logo_head.png"
    )
    main()
