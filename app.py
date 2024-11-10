# Inside the main function
def main():
    # Set up the UI with a medical theme and custom fonts
    st.markdown("""
        <style>
        .main {
            background-color: #F5F5F5;
            padding: 20px;
            border-radius: 15px;
        }
        .title {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background: linear-gradient(to right, #007BFF, #28A745); /* Blue to Green Gradient */
            color: transparent;
            -webkit-background-clip: text;
            font-size: 36px;
            text-align: center;
            font-weight: bold;
        }
        .subheader {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: #6C757D; /* Grayish Blue */
            font-size: 24px;
            text-align: center;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        }
        .button {
            background-color: #28A745; /* Fresh Green */
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .advice {
            background-color: #F0F8FF; /* Alice Blue */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .input-fields {
            background-color: #E8F5E9; /* Light Green */
            padding: 15px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header and subheader with updated medical colors
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

        # Add the submit button for the form
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
                from pydub import AudioSegment
import io

def transcribe_audio(uploaded_file):
    recognizer = sr.Recognizer()
    
    # Convert the uploaded MP3 file to WAV using pydub
    if uploaded_file.type == "audio/mp3":
        audio = AudioSegment.from_mp3(uploaded_file)
    elif uploaded_file.type == "audio/wav":
        audio = AudioSegment.from_wav(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload an MP3 or WAV file.")
        return ""
    
    # Save the converted audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=True) as temp_wav_file:
        audio.export(temp_wav_file.name, format="wav")
        with sr.AudioFile(temp_wav_file.name) as source:
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

