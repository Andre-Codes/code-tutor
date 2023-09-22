import gpt_service_web as gpt
import streamlit as st

st.set_page_config(page_title="Code Tutor - Learn Code", page_icon="👨‍🏫")

# initalize the class with role context
ct = gpt.CodeTutor()

#@st.cache
def generate_response(prompt, only_code):
    with st.spinner('Forming an answer... :thought_balloon:'):
        return ct.get_response(
            prompt = prompt,
            format_style = format_style
        )

def display_response(response, download_button, custom_header=None):
    # st.text(ct.response)
    # st.markdown(ct.complete_prompt)

    st.divider()
    if custom_header:
        st.markdown(f"# {custom_header}")
    # Create a placeholder for the markdown
    markdown_placeholder = st.empty()
    
    collected_chunks = []
    collected_responses = []
    # iterate through the stream of events
    for chunk in response:
        collected_chunks.append(chunk)  # save the event response
        if chunk['choices'][0]['finish_reason'] != 'stop':
            content_chunk = chunk['choices'][0]['delta']['content']  # extract the response
            if content_chunk:
                collected_responses.append(content_chunk)  # save the response
                formatted_response = ''.join(collected_responses)
                markdown_placeholder.markdown(f"{formatted_response}\n\n") #display the formatted chunk on the webpage
    if download_button:
        create_download(formatted_response)

def create_download(response):
    with col1:
        st.download_button(
            label=":green[Download  MD]",
            data=response,
            file_name=f'{selected_friendly_role}.md',
            mime='text/markdown'
        )  

def extra_lesson(user_prompt, role_context):
    with st.spinner('Next lesson ...'):
        # get second instruction set for continuing previous converstaion
        prompt2 = gpt.INSTRUCTIONS['role_contexts'][role_context]['instruct_2']
        messages = [user_prompt, formatted_response, prompt2]
        return messages

def handle_code_convert(user_prompt, language, language_title):
    format_style = 'code_convert'
    header = f"{language_title} translation"
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
        "Temperature", 0.0, 2.0, 0.2, 0.1
    )
    ct.temperature = round(ct.temperature * 10) / 10

convert_languages = gpt.INSTRUCTIONS['role_contexts']['code_convert']['languages']
convert_file_formats = gpt.INSTRUCTIONS['role_contexts']['code_convert']['file_formats']
convert_options = convert_languages + convert_file_formats

custom_header = None

# Sidebar with dropdown
roles = gpt.CodeTutor.get_role_contexts()
roles = {gpt.INSTRUCTIONS['role_contexts'][role]['display_name']: role for role in roles}

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
    gpt.INSTRUCTIONS['role_contexts'][selected_json_role]['button_phrase']
)

st.title(":teacher: Code Tutor")
st.subheader("How can I help you?")
prompt_box = st.empty()

# Create two columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    answer_button = st.button(
        f":blue[{button_phrase}] :sparkles:", 
        help="Generate an answer"
    )
with col2:
    if selected_json_role != 'code_convert':
        just_code_toggle = st.toggle(
            "Just code", 
            help="The result will contain only code. This is enforced when selecting 'Convert Code'.", 
            key='just_code'
        )
with col3:
    extra_lesson_toggle = st.toggle(
        "Extra lesson", 
        help="Provide additional, detailed information. Toggle this _before_ getting an answer.",
        key='extra_lesson',
        value=False
    )

user_prompt = prompt_box.text_area(
    label="How can I help?",
    label_visibility = "hidden",
    height=185,
    placeholder=gpt.INSTRUCTIONS['role_contexts'][selected_json_role]['prompt_placeholder'], 
    key='prompt'
) or None

if selected_json_role == 'code_convert':
    just_code_toggle = True
    # Display selection box for languages to convert to
    selected_language = st.sidebar.selectbox(
    "Convert to:", convert_options, format_func=lambda x: f"{x} (file format)" if x in convert_file_formats else x
    )
    convert_language = selected_language.lower().replace('-', '')
    format_style, custom_header, user_prompt = handle_code_convert(user_prompt, convert_language, selected_language)
else:
    format_style = 'markdown'

# 
if answer_button:
    # set initial actions based on user selected settings
    if ct.model == 'gpt-4':
        st.toast('Be patient. Responses from GPT-4 can be slower ...', icon="⏳")
    if user_prompt is None:
        st.info("Not sure what to ask? Creating a random lesson!", icon="🎲")
        user_prompt = "Teach me something unique and useful about Python."
        ct.role_context = 'random'
        extra_lesson_toggle = True
    
    # control whether the download button gets created
    # based on whether or not a second response will be generated
    download_button = False if extra_lesson_toggle else True

    formatted_response = ''
    # get the response from openai
    response = generate_response(user_prompt, just_code_toggle)
    display_response(response, custom_header=custom_header, download_button=download_button)
    
    if extra_lesson_toggle:
        prompt_messages = extra_lesson(user_prompt, ct.role_context)
        extra_response = generate_response(prompt_messages, just_code_toggle)
        display_response(extra_response, download_button=True, custom_header="Expanded Lesson")
        st.toast(':teacher: All Lessons Ready!', icon='✅')