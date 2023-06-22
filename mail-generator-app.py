import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/langchain/__init__.py')
from langchain import PromptTemplate

import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI


template="""
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""


prompt= PromptTemplate(input_variables=["tone","dialect","email"],template=template)


def load_llm(openai_api_key):
    llm= OpenAI(temperature=.7,openai_api_key=openai_api_key)
    return llm


st.set_page_config(page_title="Email Generator", page_icon=":robot:")
st.header("Generate Email")

col1,col2=st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format. This tool \
                is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
                [@GregKamradt](https://twitter.com/GregKamradt). \n\n View Source Code on [Github](https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py)")

with col2:
    st.image(image="TweetScreenshot.png", width=500, caption="https://twitter.com/DannyRichman/status/1598254671591723008")

st.markdown("##Enter Your Email to Convert")



def get_api_key():
    input_text=st.text_input(label="OpenAI API Key", placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text
openai_api_key=get_api_key()


col1,col2 = st.columns(2)
with col1:
    option_tone= st.selectbox("Which tone would you like your email to have?", ("Formal","Informal"))

with col2:
    option_dialect= st.selectbox("Which English dialect would you like?", ("American","English"))

def get_text():
    input_text= st.text_area(label="Email Input", label_visibility="collapsed", placeholder="Your Email...", key="email_input")
    return input_text
email_input=get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()


st.markdown("### Your Converted Email:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()
    
    llm=load_llm(openai_api_key=openai_api_key)
    prompt_with_email=prompt.format(tone=option_tone,dialect=option_dialect,email=email_input)
    formatted_email=llm(prompt_with_email)
    st.write(formatted_email)
