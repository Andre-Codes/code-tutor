import streamlit as st

# set main page configuration
ai_avatar = "pages/images/ct_logo.png"
page_title = "Code Tutor"
# use shortcodes for icons
# see: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)
page_icon = "teacher"
st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    initial_sidebar_state='expanded'
)

st.sidebar.empty()

update_message = """
**Major Update!**

 OpenAI recently announced major changes to their AI technology.
One of them, which directly affects Code Tutor, is the addition of
the **GPT-4 Turbo** model. See the *updates* section on the *welcome* page
for more information.
"""
st.sidebar.success(update_message, icon="📣")

col0, col1, col2 = st.columns([1,10,1])
with col1:
    st.write("# Welcome, I'm :green[Code Tutor]! 👋")

    st.image(ai_avatar)

    st.caption("""
    "Learning to code is like unlocking a superpower where your keyboard is the 
    cape and every line of code is a leap over the skyscrapers of digital reality." 
    -CT
    """)

st.markdown(
    """
    \n
    ### What's on the syllabus?
    ##### :books: API Analysis
    - In-depth analysis of documentation for libraries, modules, classes, and methods.
    - Simplified explanations and code examples to demonstrate usage.
    - Real-world applications and resources for further learning.
    ##### :computer: Code Assistance
    - General coding assistance; completing, debugging, and optimizing code.
    - Write completely new code based on specific instructions.
    - Quick usage examples of methods and functions from any library.
    ##### :left_speech_bubble: Code Conversion :speech_balloon:
    - Convert/translate code from one language to another.
    - Translate natural language (lines of text) to SQL queries.
    ##### :wrench: PEP 8 Formatting
    - Standardize your code to conform with Python PEP 8.
    \n
"""
)

col3, col4, col5 = st.columns([1,4,1])
with col4:
    st.markdown("**👈 Choose a room from the left** to enter :green[**the future of learning**]")

st.divider()

col6, col7, col8 = st.columns([1,3,1])
with col7:
    st.markdown("#### 🌟 Latest Updates - What's New? 🌟")
# with col7:
#     st.markdown("#### What's New? 🌟!")
#### 🌟 Latest Updates - What's New? 🌟

st.markdown(
    """
Hey Learners! We're thrilled to share the latest suite of updates. 
Our mission to make your learning journey :orange[**smoother**] 
and :orange[**smarter**] continues, and these new features are all about enhancing your experience.

##### Feature Updates:

1. **Pages:** The site is now organized in pages. The sidebar on left of the
page 👈 will include links to various *rooms*.

2. **Conversations:** Chat it up! Our new conversational AI feature allows you to 
engage in :green[**dynamic learning sessions**]. Ask questions, build upon previous ones, 
or explore new topics - the conversation flows just like it would with a real-life tutor.

3. **Code Conversion:** 
    \n\t - Converting code is even more accurate than ever. When :green[**Code Conversion**]
     is selected, the selected model will be overriden and the *GPT-4* model will be mandatory. 
     The latest models produce more accurate and efficient conversions.
    \n\t - Your :green[**natural language to SQL queries**]  just got a major performance boost. 
We've fine-tuned the translation process to ensure your instructions are 
converted into more efficient and smarter SQL statements. During testing, the
 *GPT-4 Turbo* model produced very accurate and advanced
  SQL statements even from highly complicated prompts.

4. **Persistent History:** Say goodbye to repetition. 
Our :green[**cross-page history**] functionality means that no matter where you navigate
 within Code Tutor, your dialogue and activity history follows. Seamless 
 learning without the hassle of backtracking.

*We're always working to make Code Tutor more intuitive and responsive to 
your needs. Dive in, explore the updates, and let's code smarter, not harder!*

##### Other Changes:
- The :green[**GPT-4**] model is now the *default* model. This model is
highly recommended for most code related tasks as it produces more accurate code
and follows instructions closer than previous models (i.e. gpt-3)
- The latest model :green[**GPT-4 Turbo**] has been added as an available option. This
is the most advanced model that OpenAI currently offers, and most importantly
it has *knowledge about the world up to Apr 2023*. While it is still new, 
this model is recommended for more complex coding tasks, especially
*converting code*.
- Currently the download button will save a markdown file for the *most recently 
generated response* on the page. A future update will allow downloading the entire output in 
one file from a single button on the page.
    """
)

