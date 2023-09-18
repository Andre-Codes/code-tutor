import gpt_service_web as gpt
import streamlit as st



st.title("Code Tutor")



# Sidebar with dropdown
roles = gpt.CodeTutor.get_role_contexts()
selected_fruit = st.sidebar.selectbox(
    'Select an AI Role:', 
    roles
)

# initalize the class with role context
ct = gpt.CodeTutor(
    role_context="code_help", 
    explain_level='concise', 
    comment_level='normal'
)

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

if answer_button:
    with st.spinner('Generating a response...'):
        content = ct.get_response(prompt=user_prompt, only_code=code_only_toggle)
    # display the generated markdown content
    st.divider()
    st.markdown(content)
    if extra_lesson_toggle:
        with st.spinner('Continuing lesson...'):
            # create new prompt/assistant messages
            prompt2 = gpt.INSTRUCTIONS['role_contexts'][ct.role_context]['instruct_2']
            messages = [user_prompt, ct.response_content, prompt2]
            more_content = ct.get_response(prompt=messages)
            # display the generated markdown content
            st.divider()
            st.markdown("# Further Explanation")
            st.markdown(more_content)