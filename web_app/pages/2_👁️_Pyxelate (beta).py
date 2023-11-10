import streamlit as st
import base64
import re
import os
import pages.utils.gpt_utils as gpt
from pages.utils.web_helpers import generate_response, display_response


def setup_app_config(base_path_web, base_path_local, config_file, logo_name, avatar_name):
    # Determine the base path depending on what exists
    base_path = base_path_web if os.path.exists(base_path_web) else base_path_local
    # Set up file paths uniformly
    # config_file_path = os.path.join(base_path, config_file) pages/utils/1_config.yaml
    config_file_path = "/pages/utils/2_config.yaml"
    # logo = os.path.join(base_path, logo_name)
    # avatar = os.path.join(base_path, avatar_name)
    logo = avatar = "/pages/images/ct_logo_head.png"
    # Get the API key based on the base path
    api_key = st.secrets["OPENAI_API_KEY"] if base_path == base_path_web else os.environ["OPENAI_API_KEY"]
    # Instantiate the ChatEngine
    chat_engine = gpt.ChatEngine(stream=False, api_key=api_key, config_path=config_file_path)
    # Grab the config data from the engine
    config_data = chat_engine.CONFIG

    return chat_engine, config_data, logo, avatar


def encode_image(image_file):
    bytes_data = image_file.read()
    return base64.b64encode(bytes_data).decode('utf-8')


def main():
    st.title("Visualization to Python")
    st.subheader("Convert an image to code")
    st.info("""
    This is an advanced and experimental feature. Use the **optimize** button to fix any
     generated anomalies. Use follow up chats to adjust the code to your 
     desired output. \n
     *Always test the code before using in production*.
    """, icon='⚠️')

    image_file = st.file_uploader(
        "Upload an image file",
        key='image_file',
        help=("Images can be of any data visualization such as plots, charts, "
              "graphs, or dataframe-like tables.")
    )
    st.divider()

    # Initialize the session state for chat messages
    if 'vision' not in st.session_state:
        st.session_state.setdefault('vision', {}).setdefault('messages', [])

    # Display chat history, alternating user prompt and response
    if image_file:
        for i, message in enumerate(st.session_state['vision']['messages']):
            if i % 2:
                st.chat_message('ai', avatar=ai_avatar).markdown(message)
            else:
                st.chat_message('user').text(message)

    system_role = """
       You're an expert in Python data visualizations. You will optimize,
       debug, and write efficient code for generating visualizations. The visuals
       may be dataframes, charts, graphs, etc. Always include a code snippet 
       of the complete code in your responses. You only respond to coding 
       and visualization questions.
       """

    if image_file and len(st.session_state['vision']['messages']) < 1:
        st.markdown("#### Converting the following image to code:")
        st.image(image_file)
        file_ext = image_file.type.split('/')[1]
        # MIME types don't always map directly to file extensions (e.g., 'jpeg' vs. 'jpg')
        # So, you might need a simple mapping to correct these cases
        mime_to_extension = {
            'jpeg': 'jpg',
            'png': 'png',
            'gif': 'gif',
            'bmp': 'bmp',
            'svg+xml': 'svg',
            'webp': 'webp'
        }

        file_ext = mime_to_extension.get(file_ext, file_ext)
        # Getting the base64 string
        base64_image = encode_image(image_file)
        prompt = f"data:image/{file_ext};base64,{base64_image}"

        submit_button = st.button(":blue[Pythonize]", key='submit_button')

        if submit_button:
            try:
                response_full = generate_response(chat_engine, prompt, "image_to_code")
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
                st.error(f"There was an error handling the image!\n\n{e}", icon='🚨')

        if 'code_snippet' in st.session_state:
            # Initialize the manual system role and prompt
            prompt = f"""
               For the following code, debug and/or optimize if possible. If
               the code is lacking the necessary data to display a valid plot,
               create the data, or use the built in datasets from plotting
               libraries. Include a 

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

    if image_file and len(st.session_state['vision']['messages']) > 1:
        st.sidebar.markdown("#### Original Image")
        st.sidebar.image(image_file)

        # Store the prompt and the response in a session_state list
        # for use in chatting function
        if chat_prompt := st.chat_input(placeholder="Any questions?"):
            st.chat_message('user').markdown(chat_prompt)
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
