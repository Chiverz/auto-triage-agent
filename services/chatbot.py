from agents import Agent, Runner

# Initialize the agent
agent = Agent(
    name="Assistant",
    instructions="""You are an expert business analyst working in the telecoms industry and the business stakeholder has provided you with the 1 pager business demand.

Provide what you believe to be the highest priority follow up question you would ask the business stakeholder, asking only a single question until you have no further questions and give the why?

Make sure that the question is short and focused and not overloaded so that the business stakeholder can provide a short focused response. More questions can be asked afterwards.

Ensure you explain what kind of information you are expecting so that the business stakeholder can clearly grasp what the questions are aimed at so that they can provide detailed and accurate responses.

Please note that the business stakeholder will likely have limited knowledge of technical software and integration details and is focused on the business and product delivery rather than the technical delivery.""",
)


async def chat_with_agent(chat_history):
    """Send full chat history to the AI agent for context-aware responses."""
    conversation = "\n".join(
        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}" for msg in chat_history
    )
    return await Runner.run(agent, conversation)  # Pass full history as context


def summarise_conversation(one_pager, messages):
    summary = "### 📌 Business One-Pager\n"
    for section, content in one_pager.items():
        summary += f"**{section}**\n\n{content}\n\n"

    summary += "---\n\n### 💬 Follow-up Questions & Answers\n"
    current_question = None
    for msg in messages:
        if msg["role"] == "assistant":
            current_question = msg["content"]
        elif msg["role"] == "user":
            q = current_question or "N/A"
            summary += f"**Q:** {q}\n\n**A:** {msg['content']}\n\n"
            current_question = None

    return summary


# New function to handle business requirements generation
generation_agent = Agent(
    name="RequirementsBot",
    instructions="""
As an expert business analyst, turn this business 1 pager and Q & A into a set of business requirements. Be structured and clear. Use bullet points or numbered lists where appropriate.
""",
)


async def generate_business_requirements(prompt, one_pager, messages):
    """Use a dedicated agent to generate business requirements from inputs."""
    full_context = one_pager + messages + [{"role": "user", "content": prompt}]
    conversation = "\n".join(
        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}" for msg in full_context
    )
    return await Runner.run(generation_agent, conversation)
