from agents import Agent, Runner

# Initialize the agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini",
)


async def generate_haiku(topic):
    """Generate a haiku based on the given topic using the AI agent."""
    return await Runner.run(agent, f"Write a haiku about {topic}.")
