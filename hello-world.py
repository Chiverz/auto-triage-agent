import streamlit as st
import asyncio
from haiku_generator import generate_haiku  # Import function from separate file

# Streamlit UI
st.title("AI Haiku Generator 🎴")
st.write("Ask the assistant to generate a haiku on any topic!")

# User input
user_input = st.text_input("Enter a topic for your haiku:", "recursion in programming")

# Generate haiku when button is clicked
if st.button("Generate Haiku"):
    result = asyncio.run(generate_haiku(user_input))  # Call function from haiku_generator.py
    st.write("### Generated Haiku:")
    st.write(result.final_output)
