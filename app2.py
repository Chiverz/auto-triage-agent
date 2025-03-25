import streamlit as st
import asyncio
from chatbot import chat_with_agent, summarise_conversation, generate_business_requirements

# Simple password protection
PASSWORD = st.secrets["APP_PASSWORD"]

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            st.title("Login Required")
            password = st.text_input("Enter password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted and password == PASSWORD:
                st.session_state.authenticated = True
            elif submitted:
                st.error("Incorrect password")
        return False
    return True

# Function to determine if the assistant is finished asking questions
def assistant_is_done(message):
    done_phrases = [
        "no further questions",
        "that's all I need",
        "thank you for the answers"
    ]
    return any(phrase in message.lower() for phrase in done_phrases)

# Function to display a rich-text-like summary
def show_summary():
    st.title("📄 Business Analyst Summary")
    st.markdown("Here is a summary of your one-pager and the assistant's follow-up conversation:")

    summary_text = summarise_conversation(
        one_pager={
            'Title' : st.session_state.title_of_change,
            'Reason for Change': st.session_state.reason_for_change,
            'Vision & Objectives': st.session_state.vision_objectives,
            'Known Risks & Challenges': st.session_state.risks_challenges,
            'Aspirational Delivery Date': st.session_state.delivery_date,
            'Non-Quantifiable Benefits & Justifications': st.session_state.benefits_justifications,
            'Measurement of Benefits': st.session_state.measure_benefits,
        },
        messages=st.session_state.messages
    )

    st.markdown(summary_text)

    st.markdown("---")
    st.subheader("Generated Business Requirements")
    with st.spinner("Generating business requirements..."):
        requirements = asyncio.run(generate_business_requirements(
            prompt="As an expert business analyst, turn this business 1 pager and Q & A into a set of business requirements.",
            one_pager=st.session_state.one_pager,
            messages=st.session_state.messages
        ))
        st.markdown(requirements)

# Define the initial form to collect user inputs
def show_initial_form():
    st.title("Auto Triage Form")
    st.write("Please complete the business 1 pager form.")
  
    with st.form(key='initial_form'):
        title_of_change = st.text_area("Title", value="""Uninhabitables""")
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
        st.session_state.title_of_change = title_of_change
        st.session_state.reason_for_change = reason_for_change
        st.session_state.vision_objectives = vision_objectives
        st.session_state.risks_challenges = risks_challenges
        st.session_state.delivery_date = delivery_date
        st.session_state.benefits_justifications = benefits_justifications
        st.session_state.measure_benefits = measure_benefits

        # Store business content separately
        st.session_state.one_pager = [
            {"role": "system", "content": f"Title: {title_of_change}"},
            {"role": "system", "content": f"Reason for Change: {reason_for_change}"},
            {"role": "system", "content": f"Vision & Objectives: {vision_objectives}"},
            {"role": "system", "content": f"Known Risks & Challenges: {risks_challenges}"},
            {"role": "system", "content": f"Aspirational Delivery Date: {delivery_date}"},
            {"role": "system", "content": f"Non-Quantifiable Benefits & Justifications: {benefits_justifications}"},
            {"role": "system", "content": f"Measurement of Benefits: {measure_benefits}"}
        ]

        # Start fresh conversation with instruction only
        st.session_state.messages = [
            {"role": "system", "content": "You are an expert business analyst working in the telecoms industry. The business stakeholder has provided you with the 1-pager business demand. Provide what you believe to be the highest priority follow-up question to ask the business stakeholder, until you have no further questions — and give the 'why'."}
        ] + st.session_state.one_pager

        st.session_state.chat_mode = True

        response = asyncio.run(chat_with_agent(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": response.final_output})

        st.rerun()

def show_chat_interface():
    
    st.markdown("---")
    if len([m for m in st.session_state.messages if m['role'] == 'assistant']) >= 2 and st.button("✅ Finish Q&A and Generate Requirements"):
        st.session_state.chat_mode = False
        st.session_state.chat_complete = True
        st.rerun()
    st.title("Auto Triage Q & A")
    st.write("The assistant will ask follow-up questions based on your provided information.")

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").markdown(message["content"])

    if prompt := st.chat_input("Your response:"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = asyncio.run(chat_with_agent(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": response.final_output})

        if assistant_is_done(response.final_output):
            st.session_state.chat_mode = False
            st.session_state.chat_complete = True

        st.rerun()

def main():
    if not check_password():
        return

    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = False
    if 'chat_complete' not in st.session_state:
        st.session_state.chat_complete = False

    if st.session_state.chat_complete:
        show_summary()
    elif st.session_state.chat_mode:
        show_chat_interface()
    else:
        show_initial_form()

if __name__ == "__main__":
    main()
