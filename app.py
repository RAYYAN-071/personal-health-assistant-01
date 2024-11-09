# Install required libraries

# Import necessary modules
import os
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from groq import Groq
import tempfile
import IPython.display as ipd

# Configure the Groq client
client = Groq(api_key="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")

# Streamlit app
def main():
    # Set up the UI with an eye-catching theme and custom fonts
    st.markdown("""
        <style>
        .main {
            background-color: #F5F5F5;
            padding: 20px;
            border-radius: 15px;
        }
        .title {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: #FF6347; /* Tomato red */
            font-size: 36px;
            text-align: center;
        }
        .subheader {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: #FFD700; /* Vibrant yellow */
            font-size: 24px;
            text-align: center;
        }
        .button {
            background-color: #FF1493; /* Deep pink */
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .advice {
            background-color: #FFFACD; /* Lemon chiffon */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .input-fields {
            background-color: #F0FFF0; /* Honeydew */
            padding: 15px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header and subheader with medical emoji
    st.markdown('<p class="title">💊 Personal Health Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Get personalized health advice, diet suggestions, and precautions.</p>', unsafe_allow_html=True)

    # Input fields for user to type their age and describe their condition
    with st.form("health_form", clear_on_submit=True):
        st.markdown('<div class="input-fields">', unsafe_allow_html=True)
        age = st.text_input("Enter Your Age", placeholder="e.g., 25")
        condition = st.text_area("Describe Your Condition", placeholder="e.g., I have a fever and headache.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Audio file upload
        uploaded_file = st.file_uploader("Upload Your Audio (MP3, WAV)", type=["mp3", "wav"])

        if uploaded_file is not None:
            # Convert the uploaded audio to text
            condition = transcribe_audio(uploaded_file)

        # Advice button to get the response from the model
        submit_button = st.form_submit_button("Get Advice")
        
        if submit_button:
            if age and condition:
                # Define the prompt for the Llama model based on user input
                user_message = f"Patient details: Age: {age}, Condition: {condition}. Provide medical advice, dietary recommendations, and necessary precautions."

                # Use Groq's chat completion API
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": user_message}],
                    model="llama3-8b-8192",
                )

                # Extract and display the model's response
                response = chat_completion.choices[0].message.content

                # Display the advice and recommendations in a styled box
                st.markdown('<div class="advice">', unsafe_allow_html=True)
                st.write("### Advice and Recommendations:")
                st.write(response)
                st.markdown('</div>', unsafe_allow_html=True)

                # Text-to-speech for chatbot response (using gTTS)
                speak_response(response)
            else:
                st.warning("Please enter both your age and condition to get advice.")

# Function to transcribe uploaded audio
def transcribe_audio(uploaded_file):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(uploaded_file)
    with audio as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, could not understand the audio.")
            return ""
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

# Function for text-to-speech (using gTTS)
def speak_response(response):
    # Convert the text to speech using Google Text-to-Speech (gTTS)
    tts = gTTS(text=response, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio:
        tts.save(temp_audio.name)
        audio_file = temp_audio.name
        st.audio(audio_file, format="audio/mp3")

# Run the Streamlit app
if __name__ == "__main__":
    main()
