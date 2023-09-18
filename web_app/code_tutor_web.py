import gpt_service_web as gpt
import streamlit as st



st.title("Code Tutor")

# Sidebar with dropdown
roles = gpt.CodeTutor.get_role_contexts()
selected_fruit = st.sidebar.selectbox(
    'Select an AI Role:', 
    roles
)

prompt_box = st.empty()
user_prompt = prompt_box.text_area("Enter a prompt", 
                     placeholder="Prompt...",
                     key='prompt')


ct = gpt.CodeTutor(
    role_context="pep8", 
    explain_level='concise', 
    comment_level='normal',
    model='gpt-4'
)



if st.button("Answer"):
    with st.spinner('Generating a response...'):
        content = ct.get_response(prompt=user_prompt)
    
    st.markdown(content, unsafe_allow_html=True)

    