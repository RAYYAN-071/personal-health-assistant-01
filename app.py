# Install required libraries
!pip install streamlit groq

# Import necessary modules
import os
import streamlit as st
from groq import Groq

# Configure the Groq client
client = Groq(api_key="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")

# Streamlit app
def main():
    # Set up the UI
    st.title("Personal Health Assistant")
    st.subheader("Get personalized health advice")

    # Dropdown for age
    age = st.selectbox("Select Your Age", options=[str(i) for i in range(18, 101)], index=10)
    # Dropdown for condition
    condition = st.selectbox("Select Your Condition", options=["Healthy", "Fever", "Diabetes", "Hypertension", "Other"])

    # Get advice button
    if st.button("Get Advice"):
        # Define the prompt for the Llama model based on user input
        user_message = f"Patient details: Age: {age}, Condition: {condition}. Provide medical advice, dietary recommendations, and necessary precautions."

        # Use Groq's chat completion API
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama3-8b-8192",
        )

        # Extract and display the model's response
        response = chat_completion.choices[0].message.content
        st.write("### Advice and Recommendations")
        st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()
