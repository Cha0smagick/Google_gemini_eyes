import streamlit as st
from PIL import Image
import textwrap
import google.generativeai as genai

# Function to display formatted Markdown text
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Function to generate content using Gemini API
def generate_gemini_content(prompt, model_name='gemini-pro', image=None):
    model = genai.GenerativeModel(model_name)
    if model_name == 'gemini-pro-vision' and not image:
        st.warning("Please add an image to use the gemini-pro-vision model.")
        return None

    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)

    return response

# Streamlit app
def main():
    st.title("Gemini API Demo with Streamlit")

    # Get Gemini API key from user input
    api_key = st.text_input("Enter your Gemini API key:")
    genai.configure(api_key=api_key)

    # Choose a model
    model_name = st.selectbox("Select a Gemini model", ["gemini-pro", "gemini-pro-vision"])

    # Get user input prompt
    prompt = st.text_area("Enter your prompt:")

    # Get optional image input
    image_file = st.file_uploader("Upload an image (if applicable):", type=["jpg", "jpeg", "png"])

    # Display image if provided
    if image_file:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)

    # Generate content on button click
    if st.button("Generate Content"):
        st.markdown("### Generated Content:")
        if model_name == 'gemini-pro-vision':
            if not image_file:
                st.warning("Please provide an image for the gemini-pro-vision model.")
            else:
                image = Image.open(image_file)
                response = generate_gemini_content(prompt, model_name=model_name, image=image)
        else:
            response = generate_gemini_content(prompt, model_name=model_name)

        # Display the generated content in Markdown format if response is available
        if response:
            if response.candidates:
                parts = response.candidates[0].content.parts
                generated_text = parts[0].text if parts else "No content generated."
                st.markdown(to_markdown(generated_text))
            else:
                st.warning("No candidates found in the response.")

if __name__ == "__main__":
    main()
