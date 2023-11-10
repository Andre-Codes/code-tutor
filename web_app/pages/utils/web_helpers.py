import streamlit as st
import json


ai_avatar = "/mount/src/code-tutor/web_app/pages/images/ct_logo_head.png"  # /app/code-tutor/web_app/


def generate_response(app, prompt, role_context=None, **kwargs):
    if prompt is None:
        raise ValueError("No prompt provided.")
    param_configs = {
        'code_convert': {'prompt': prompt, 'system_role': app.system_role},
        'quiz': {'prompt': prompt, 'format_style': 'json'},
        'image_to_code': {'prompt': prompt, 'response_type': 'vision', 'raw_output': False}
    }
    with st.spinner('...thinking :thought_balloon:'):
        try:
            # Use the dictionary to get the appropriate parameters
            params = param_configs.get(role_context, {'prompt': prompt})
            # Update params with any additional kwargs provided
            params.update(kwargs)
            # Call the get_response method with the unpacked parameters
            response = app.get_response(**params)
            return response
        except Exception as e:
            raise e


def handle_file_output(responses):
    all_response_content = [f"{responses} \n\n"]
    file_data = ''.join(all_response_content)
    return file_data


def create_download(response, role_name):
    st.download_button(
        label=":green[Download] :floppy_disk:",
        data=response,
        file_name=f'{role_name}.md',
        mime='text/markdown'
    )


def display_response(response, streaming, download=True, role_name=None):
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
                    markdown_placeholder.chat_message('ai', avatar=ai_avatar).markdown(f"{response_content}🖋️\n\n")
            else:
                markdown_placeholder.chat_message('ai', avatar=ai_avatar).markdown(response_content)
    elif role_name == 'quiz':
        response_content = response['choices'][0]['message']['content']
        json_content = json.loads(response_content)
        for i, q in enumerate(json_content['questions']):
            st.markdown(f"#### {q['question']}")
            if 'code' in q:
                st.code(q['code'])
            choices = st.radio(label="Choices", options=q['choices'], label_visibility='hidden', key=i)
            result_placeholder = st.empty()
    else:
        response_content = response['choices'][0]['message']['content']
        markdown_placeholder.markdown(response_content)
        file_data = response_content

    file_data = handle_file_output(response_content)  # not working with extra lesson

    if download:
        create_download(file_data, role_name)

    return response_content
