import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome, I'm :green[Code Tutor]! 👋")
st.subheader("Your trusty AI :blue[coding assistant]")

st.image("pages/images/ct_logo.png")
st.caption("""
"Learning to code is like unlocking a superpower where your keyboard is the 
cape and every line of code is a leap over the skyscrapers of digital reality." 
-CT
""")
st.markdown(
    """
    \n
    **👈 Enter a room from the sidebar** to begin your learning experience!
    
    ##### Here's a taste of what I can do...
    1. :books: *Summarize* and explain complex API documentation, provide several code
    examples, and cite any helpful resources.
    2. :computer: *Assist* with completing, debugging, and optimizing any of your code, 
    writing completely new code based on your instructions, or simply answering
    any general code related question.
    3. :left_speech_bubble: *Translate* code from one language to another
    4. :wrench: *Standardize* your code to conform with Python PEP 8. 
"""
)

