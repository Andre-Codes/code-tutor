import streamlit as st


ai_avatar = "ct_logo_head.png"  # /app/code-tutor/web_app/

def generate_response(app, prompt, role_context):
    if prompt is None:
        raise ValueError("No prompt provided.")
    with st.spinner('...thinking :thought_balloon:'):
        try:
            # override system role with customized role
            if role_context == 'code_convert':
                response = app.get_response(prompt=prompt, system_role=app.system_role)
                return response
            else:
                response = app.get_response(prompt=prompt)
                return response
        except Exception as e:
            raise e


def handle_file_output(responses):
    all_response_content = []
    all_response_content.append(f"{responses} \n\n")
    file_data = ''.join(all_response_content)
    return file_data


def create_download(response, role_name):
    st.download_button(
        label=":green[Download] :floppy_disk:",
        data=response,
        file_name=f'{role_name}.md',
        mime='text/markdown'
    )


def display_response(response, download, role_name, streaming):
    st.divider()
    markdown_placeholder = st.empty()
    collected_responses = []

    if streaming:
        for chunk in response:
            if chunk['choices'][0]['finish_reason'] != 'stop':
                content_chunk = chunk['choices'][0]['delta']['content']
                if content_chunk:
                    collected_responses.append(content_chunk)
                    response_content = ''.join(collected_responses)
                    # TODO: use st.chat_message('ai').markdown
                    markdown_placeholder.chat_message('ai', avatar=ai_avatar).markdown(f"{response_content}🖋️\n\n")
            else:
                markdown_placeholder.chat_message('ai', avatar=ai_avatar).markdown(response_content)

    else:
        response_content = response['choices'][0]['message']['content']
        markdown_placeholder.markdown(response_content)
        file_data = response_content

    file_data = handle_file_output(response_content)  # not working with extra lesson

    if download:
        create_download(file_data, role_name)

    return response_content
