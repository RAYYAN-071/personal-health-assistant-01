# Install required libraries

# Import necessary modules
import os
import streamlit as st
from groq import Groq

# Configure the Groq client
client = Groq(api_key="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")

# Streamlit app
def main():
    # Set up the UI with an eye-catching theme
    st.markdown("""
        <style>
        .main {
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 10px;
        }
        .title {
            color: #1e90ff;
            font-size: 36px;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        .subheader {
            color: #4682b4;
            font-size: 24px;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        .button {
            background-color: #4682b4;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .advice {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header and subheader for the page
    st.markdown('<p class="title">Personal Health Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Get personalized health advice, diet suggestions, and precautions.</p>', unsafe_allow_html=True)

    # Input fields for user to type their age and describe their condition
    age = st.text_input("Enter Your Age", placeholder="e.g., 25")
    condition = st.text_area("Describe Your Condition", placeholder="e.g., I have a fever and headache.")

    # Advice button to get the response from the model
    if st.button("Get Advice", key="generate_advice"):
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
        else:
            st.warning("Please enter both your age and condition to get advice.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
