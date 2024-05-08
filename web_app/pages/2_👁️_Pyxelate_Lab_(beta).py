import streamlit as st
import base64
import re
import os
from pathlib import Path
import pages.utils.gpt_utils as gpt
from pages.utils.web_helpers import generate_response, display_response


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


def encode_image(image_file):
    bytes_data = image_file.read()
    return base64.b64encode(bytes_data).decode('utf-8')


def clear_chat():
    # Delete all generated image related items in Session state
    if 'vision' in st.session_state:
        del st.session_state['vision']
    if 'code_snippet' in st.session_state:
        del st.session_state['code_snippet']


def main():
    st.title("Visualization to Python")
    st.subheader("Convert an image to code")
    st.caption("*Code Tutor has optimized this feature to work specifically with data visualizations.*")
    st.info("""
    This is an advanced and experimental feature. Use the **optimize** button to fix any
     generated anomalies. Use follow up chats to adjust the code to your 
     desired output. \n
     *Always test the code before using in production*.
    """, icon='⚠️')

    image_file = st.file_uploader(
        label="Upload an image file (PNG, JPG, WEBP, or GIF)",
        key='image_file',
        on_change=clear_chat,
        help=("Images can be of any data visualization such as plots, charts, "
              "graphs, or dataframe-like tables.")
    )
    image_url = st.text_input(
        label="Or enter an image URL",
        key='image_url',
        on_change=clear_chat,
        help=("URL to any data visualization such as plots, charts, "
              "graphs, or dataframe-like tables.")
    )
    st.divider()

    # Initialize the session state for images and chat
    if 'vision' not in st.session_state:
        st.session_state.setdefault('vision', {}).setdefault('messages', [])
    if 'saved_image' not in st.session_state:
        st.session_state.saved_image = None

    # Display chat history, alternating user prompt and response
    if st.session_state.saved_image:
        for i, message in enumerate(st.session_state['vision']['messages']):
            if i % 2:
                st.chat_message('ai', avatar=ai_avatar).markdown(message)
            else:
                st.chat_message('user').text(message)

    system_role = """
       You're an expert in Python data visualizations. You will optimize,
       debug, and write efficient code for generating visualizations. The visuals
       may be dataframes, charts, graphs, etc. Always include a code snippet 
       of the complete code in your responses even if no changes were made. 
       You only respond to coding and visualization questions.
       """

    if len(st.session_state['vision']['messages']) < 1:
        if image_file:
            # Save the uploaded image to session state
            st.session_state.saved_image = image_file
            # Display the image file
            st.image(image_file)
            # Extract file extension
            file_ext = image_file.type.split('/')[1]
            # MIME types to file ext. mapping
            mime_to_extension = {
                'jpeg': 'jpg',
                'png': 'png',
                'gif': 'gif',
                'bmp': 'bmp',
                'svg+xml': 'svg',
                'webp': 'webp'
            }
            # Get the MIME type from the type to ext. dict
            file_ext = mime_to_extension.get(file_ext, file_ext)
            # Getting the base64 string
            base64_image = encode_image(image_file)
            prompt = f"data:image/{file_ext};base64,{base64_image}"

        if image_url:
            # Save the uploaded image to session state
            st.session_state.saved_image = image_url
            # Display the image from URL
            st.image(image_url)
            prompt = image_url

        if st.session_state.saved_image:
            if submit_button := st.button(":blue[Pythonize]", key='submit_button'):
                try:
                    response_full = generate_response(chat_engine, prompt, role_context="image_to_code")
                    st.divider()
                    # Extract python code from markdown
                    pattern = r"```python\n(.*?)```"
                    code_snippet = re.findall(pattern, response_full, re.DOTALL)
                    if code_snippet:
                        st.session_state['code_snippet'] = code_snippet[0]
                    if response_full:
                        st.markdown("#### Pythonized image:")
                        st.markdown(response_full)
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
                        st.error(f"There was an error handling the image!\n\n{error_message}", icon='🚨')

        if 'code_snippet' in st.session_state:
            # Initialize the manual system role and prompt
            prompt = f"""
               For the following code, debug and/or optimize if possible.
               Check if the correct usage for methods and parameters are in place.  
               If the desired visual can be produced using more advanced 
               or appropriate plotting methods, update the code accordingly. If
               the code is lacking the necessary data to display a valid plot,
               create the data, or use the built in datasets from plotting
               libraries, i.e. load_dataset() method:

               {st.session_state['code_snippet']}
               """

            if optimize_button := st.button(
                    label=":blue[Optimize & Explain]",
                    help="""
                    The interpreted code may not be accurate. Press this button to
                    submit this code for revision and a breakdown of how it works.
                    """):
                response = generate_response(
                    chat_engine,
                    prompt,
                    streaming=True,
                    system_role=system_role
                )

                response = display_response(
                    response,
                    streaming=True,
                    download=False
                )

                st.session_state['vision']['messages'].append(st.session_state['code_snippet'])
                st.session_state['vision']['messages'].append(response)

    if st.session_state.saved_image and len(st.session_state['vision']['messages']) > 1:
        st.sidebar.markdown("#### Original Image")
        st.sidebar.image(st.session_state.saved_image)

        # Store the prompt and the response in a session_state list
        # for use in chatting function
        if chat_prompt := st.chat_input(placeholder="Any questions?"):
            st.chat_message('user').text(chat_prompt)
            st.session_state['vision']['messages'].append(chat_prompt)

            response_2 = generate_response(
                chat_engine,
                prompt=st.session_state['vision']['messages'],
                streaming=True,
                system_role=system_role
            )

            response_2 = display_response(
                response_2,
                streaming=True,
                download=False
            )
            st.session_state['vision']['messages'].append(response_2)

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


if __name__ == '__main__':
    # create the chat engine instance and retrieve the custom configuration data
    chat_engine, config_data, page_logo, ai_avatar = setup_app_config(
        base_path_web="/mount/src/code-tutor/web_app/pages/",  # streamlit server path
        base_path_local="pages/",  # local path
        config_file="utils/2_config.yaml",
        logo_name="images/ct_logo_head.png",
        avatar_name="images/ct_logo_head.png"
    )
    main()
