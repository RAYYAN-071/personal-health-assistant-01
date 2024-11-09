# Install required libraries

# Import necessary modules
import os
import streamlit as st
import pyttsx3
import speech_recognition as sr
from groq import Groq

# Configure the Groq client
client = Groq(api_key="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")

# Initialize text-to-speech engine
engine = pyttsx3.init()

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

        # Audio recording and speech-to-text
        if st.button("Record Your Condition (Audio)"):
            st.write("Recording your voice, please speak clearly.")
            with st.spinner("Recording..."):
                condition = record_audio()

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

                # Text-to-speech for chatbot response
                speak_response(response)
            else:
                st.warning("Please enter both your age and condition to get advice.")

# Function for recording audio and converting to text
def record_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
    except Exception as e:
        st.error("Sorry, I couldn't understand the audio.")
        return ""

# Function for text-to-speech
def speak_response(response):
    engine.say(response)
    engine.runAndWait()

# Run the Streamlit app
if __name__ == "__main__":
    main()
