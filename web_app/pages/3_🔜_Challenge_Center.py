import streamlit as st
import os
import json
import random
import pages.utils.gpt_utils as gpt
from pages.utils.web_helpers import generate_response


# set main page configuration
page_title = "Challenge Center"
# use shortcodes for icons
# see: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)
page_icon = "100"

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    initial_sidebar_state='expanded'
)


def display_response(response):
    st.divider()
    question_container = st.container()

    with question_container:
        for i, q in enumerate(response):
            # Display the questions
            st.markdown(f"#### {q['question']}")
            # Display any code snippets
            if 'code' in q:
                st.code(q['code'])
            # Display and choices, save selected answer
            st.session_state['answers'][i] = st.radio(
                label="Choices",
                options=q['choices'],
                label_visibility='hidden',
                key=f"question_{i}"
            )

            result_placeholder = st.empty()

    # if download:
    #     create_download(file_data, role_name)


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
        if chat_engine.model == 'gpt-4':
            st.toast('Be patient. Responses from GPT-4 can be slower...', icon="⏳")

        response = generate_response(chat_engine, prompt, chat_engine.role_context)

        response_content = response['choices'][0]['message']['content']
        json_response = json.loads(response_content)

        display_response(json_response['questions'])

        if 'questions' not in st.session_state:
            st.session_state['questions'] = json_response['questions']

        st.toast(':teacher: All replies ready!', icon='✅')

        return json_response, prompt

    except Exception as e:
        raise e


# def generate_response(app, prompt, role_context):
#     if prompt is None:
#         raise ValueError("No prompt provided.")
#     with st.spinner('...crafting quiz :nerd_face:'):
#         try:
#             response = app.get_response(prompt=prompt, format_style='json')
#             return response
#         except Exception as e:
#             raise e


def create_download(response, role_name):
    st.download_button(
        label=":green[Download] :floppy_disk:",
        data=response,
        file_name=f'{role_name}.md',
        mime='text/markdown'
    )


# Function to set up the app configurations
# @st.cache_data
def setup_app_config(base_path_web, base_path_local, config_file, logo_name, avatar_name):
    # Determine the base path depending on what exists
    base_path = base_path_web if os.path.exists(base_path_web) else base_path_local
    # Set up file paths uniformly
    # config_file_path = os.path.join(base_path, config_file) pages/utils/1_config.yaml
    config_file_path = "/mount/src/code-tutor/web_app/pages/utils/2_config.yaml"  # /mount/src/code-tutor/web_app/
    # logo = os.path.join(base_path, logo_name)
    # avatar = os.path.join(base_path, avatar_name)
    logo = avatar = "/mount/src/code-tutor/web_app/pages/images/ct_logo_head.png"
    # Get the API key based on the base path
    api_key = st.secrets["OPENAI_API_KEY"] if base_path == base_path_web else os.environ["OPENAI_API_KEY"]
    # Instantiate the ChatEngine
    chat_engine = gpt.ChatEngine(stream=True, api_key=api_key, config_path=config_file_path)
    # Grab the config data from the engine
    config_data = chat_engine.CONFIG

    return chat_engine, config_data, logo, avatar


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
        'allow_null_prompt': config_data['app_ui']['prompt']['allow_null_prompt'],

        # Sidebar Controls
        'api_key': config_data['app_ui']['sidebar']['api_key'],
        'adv_settings': config_data['app_ui']['sidebar']['adv_settings'],
        'role_context': config_data['app_ui']['sidebar']['role_context'],

        'all_role_contexts': config_data['role_contexts']
    }
    return config_settings


def setup_app_controls(app_config):
    st.title(f":gray[{app_config['app_title']}]")
    st.subheader(f":construction: :red[{app_config['subheader']}] :construction:")

    prompt_box = st.empty()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        response_button = st.button(
            f":blue[Create Quiz] :sparkles:",
            help="Generate an answer",
            disabled=not app_config['response_button']  # inverse of enabled status
        )

    chat_engine.user_prompt = prompt_box.text_area(
        label="Enter a prompt",
        label_visibility="visible",
        height=185,
        placeholder=app_config['all_role_contexts']['quiz']['prompt_placeholder'],
        key='prompt',
        disabled= not app_config['prompt_box'],
        help="""
        Entering in a prompt here will always start a new quiz. 
        After conversing with Code Tutor, you can return here at 
        any time to start a new quiz without removing any previous ones.
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

    if app_config['api_key']:
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
            llm_model = st.selectbox(
                "Model",
                ["GPT-3", "GPT-4", "GPT-4 Turbo"],
                index=0,
                help="""
                GPT-3: very fast, streamlined responses, yet prone to mistakes.
                 | GPT-4: slower response, yet better accuracy and attention 
                 to detail, especially with code.
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
    if app_config['role_context']:
        selected_friendly_role = role_context.selectbox('Prompt Context :memo:', roles.keys())
        selected_role = roles[selected_friendly_role]
    else:
        #  Manually set role variables
        selected_friendly_role = "Pop Quiz!"
        selected_role = roles[selected_friendly_role]

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


def main():
    config_settings = load_app_config()
    # save the selected AI context, role name
    chat_engine.role_context, selected_friendly_role = setup_sidebar(chat_engine, config_settings)
    # Manually set context until future additions
    context = 'quiz'

    chat_engine.user_prompt, response_button = setup_app_controls(config_settings)
    # Initialize session state

    if 'questions' in st.session_state:
        display_response(st.session_state['questions'])

    if 'answers' not in st.session_state:
        st.session_state['answers'] = [None] * 10

    if response_button:
        try:
            handle_response(chat_engine, context,
                            config_settings, prompt=chat_engine.user_prompt)
            # st.session_state[context]['messages'].append(prompt)
            # st.session_state[context]['messages'].append(response)
        except Exception as e:
            st.error(f"There was an error handling your question!\n\n{e}", icon='🚨')

    # if st.button("Submit"):
    #     correct_answers = sum(st.session_state['answers'][i] == questions[i]["answer"] for i in range(len(questions)))
    #     st.write(f"You got {correct_answers} out of {len(questions)} correct!")


if __name__ == '__main__':
    # create the chat engine instance and retrieve the custom configuration data
    chat_engine, config_data, page_logo, ai_avatar = setup_app_config(
        base_path_web="/app/code-tutor/web_app/pages/",  # streamlit server path
        base_path_local="pages/",  # local path
        config_file="utils/2_config.yaml",
        logo_name="images/ct_logo_head.png",
        avatar_name="images/ct_logo_head.png"
    )
    main()
