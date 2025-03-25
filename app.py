import streamlit as st
import asyncio
from chatbot import chat_with_agent  # Import the chat function

# Define the initial form to collect user inputs
def show_initial_form():
    with st.form(key='initial_form'):
        reason_for_change = st.text_area("Reason for Change?", value="""Uninhabitable locations require a separate order journey when compared to the current standard ordering journey we have built.
TalkTalk require the ability to be able to place SOGEA and FTTP orders to Uninhabitable sites via SOM2.""")
        vision_objectives = st.text_area("The Vision & Objectives", value="Allow Partners to place orders for Uninhabitable locations such as Traffic lights, oyster card terminals etc.")
        risks_challenges = st.text_area("Known Risks & Challenges", value="""We used to order WLR to uninhabitable premises however, WLR stop sell came into affect on the 5th September. 
As we haven’t built this into SOGEA and FTTP joruneys, we don’t have a product available to sell which could result in losing business.""")
        delivery_date = st.text_area("Aspirational Delivery Date and why", value="Ideally, we need this by September 5th. As this isn’t achievable, early next year would be a good target.")
        benefits_justifications = st.text_area("Non-Quantifiable Benefits & Justifications", value="""Partner satisfaction
Reduce risk of partner churn
Continue to sell to uninhabitable premises after WLR closure""")
        measure_benefits = st.text_area("How are you going to measure the benefits?", value="Uninhabitable orders placed.")
        
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Store the inputs in session state
        st.session_state.reason_for_change = reason_for_change
        st.session_state.vision_objectives = vision_objectives
        st.session_state.risks_challenges = risks_challenges
        st.session_state.delivery_date = delivery_date
        st.session_state.benefits_justifications = benefits_justifications
        st.session_state.measure_benefits = measure_benefits
        
        # Initialize chat history with the collected information
        st.session_state.messages = [
            {"role": "system", "content": f"Reason for Change: {reason_for_change}"},
            {"role": "system", "content": f"Vision & Objectives: {vision_objectives}"},
            {"role": "system", "content": f"Known Risks & Challenges: {risks_challenges}"},
            {"role": "system", "content": f"Aspirational Delivery Date: {delivery_date}"},
            {"role": "system", "content": f"Non-Quantifiable Benefits & Justifications: {benefits_justifications}"},
            {"role": "system", "content": f"Measurement of Benefits: {measure_benefits}"}
        ]
        
        # Transition to chat mode
        st.session_state.chat_mode = True

        # Generate the first follow-up question
        response = asyncio.run(chat_with_agent(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": response.final_output})
        
        st.rerun()

# Define the chat interface
def show_chat_interface():
    st.title("Chat with AI 🤖")
    st.write("The assistant will ask follow-up questions based on your provided information.")

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])

    # User input box
    if prompt := st.chat_input("Your response:"):
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI response
        response = asyncio.run(chat_with_agent(st.session_state.messages))

        # Append AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.final_output})

        # Refresh the UI to display the new messages
        st.rerun()

# Main function to control the app flow
def main():
    # Initialize chat_mode in session state if not already set
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = False

    # Display the appropriate interface based on the chat_mode
    if st.session_state.chat_mode:
        show_chat_interface()
    else:
        show_initial_form()

if __name__ == "__main__":
    main()
