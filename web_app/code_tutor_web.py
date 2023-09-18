import gpt_service_web as gpt
import streamlit as st




# initalize the class with role context
ct = gpt.CodeTutor(
    role_context="code_help", 
    explain_level='concise', 
    comment_level='normal'
)

# Sidebar with dropdown
roles = gpt.CodeTutor.get_role_contexts()

def generate_response(prompt, only_code):
    with st.spinner('Generating a response...'):
        return ct.get_response(prompt=prompt, only_code=only_code)

def display_content(content, header=None):
    st.divider()
    with st.container():
        if header:
            st.markdown(f"# {header}")
        st.markdown(content)

def extra_lesson(user_prompt, role_context):
    with st.spinner('Continuing lesson...'):
        prompt2 = gpt.INSTRUCTIONS['role_contexts'][role_context]['instruct_2']
        messages = [user_prompt, ct.response_content, prompt2]
        return ct.get_response(prompt=messages)

selected_role = st.sidebar.selectbox(
    'Select an AI Role:', 
    roles
)

st.title("Code Tutor")

prompt_box = st.empty()

# Create two columns
col1, col2, col3 = st.columns(3)

with col1:
    answer_button = st.button("Teach")
with col2:
    code_only_toggle = st.toggle("Just code")
with col3:
    extra_lesson_toggle = st.toggle("Extra lesson")

user_prompt = prompt_box.text_area(
    label="Enter your prompt", 
    placeholder="How do I loop through a dictionary . . .", 
    key='prompt'
)

# 
if answer_button:
    content = generate_response(user_prompt, code_only_toggle)
    display_content(content)
    
    if extra_lesson_toggle:
        more_content = extra_lesson(user_prompt, ct.role_context)
        display_content(more_content, header="Further Explanation")
            
            