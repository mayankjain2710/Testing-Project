import speech_recognition as sr
import streamlit as st
from pydub import AudioSegment
from pydub.playback import play
import os
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
from IPython.display import Markdown

# Load environment variables from .env
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to convert bullet points to Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Initialize recognizer for speech recognition
r = sr.Recognizer()

# Function to record speech and convert to text
def record_text():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            st.write("Listening...")
            audio2 = r.listen(source2)
            st.write("Processing...")
            MyText = r.recognize_google(audio2)
            return MyText

    except sr.RequestError as e:
        st.write("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        st.write("Unknown error occurred")

# Function to get Gemini response
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Shiksha Saarthi")
st.header("SHIKSHA SAARTHI")

# Check if session state exists for storing input
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''

# Button to record speech
if st.button("Speak to Agent"):
    speech_input = record_text()
    if speech_input:
        st.session_state['input_text'] = speech_input  # Save speech to session state

# Input text box as fallback, filled with speech input if available
input_text = st.text_input("Input:", value=st.session_state['input_text'])

# Button to submit query
submit = st.button("Proceed")

# If submit button is clicked
if submit:
    if not input_text:
        st.write("No input provided.")
    else:
        # Get response from Gemini Pro
        response = get_gemini_response(input_text)
        st.subheader("The Response is")
        st.write(response)
