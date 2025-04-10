from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain.agents import Tool, initialize_agent
from pydantic import BaseModel, Field
from typing import Optional, List

# Marketing system state definition
class MarketingState(TypedDict):
    question: str                     # User's marketing request
    marketing_posts: List[str]        # Initial generated posts
    revision_feedback: Optional[str]  # Feedback for revisions
    final_posts: Optional[List[str]]  # Revised posts

# Agent for generating initial marketing posts
marketing_content_prefix = (
    "You are the MarketingContentAgent, a specialist in creating social media content. "
    "Generate three social media posts in an authentic, creative style full of energy, hashtags, and modern expressions. Be concise."
)
marketing_content_system_message = SystemMessage(content=marketing_content_prefix)
marketing_content_agent = create_react_agent(
    model="gpt-3.5-turbo-1106",
    tools=[]
)

# Agent for revising marketing posts based on feedback
marketing_revision_prefix = (
    "You are the MarketingRevisionAgent, a specialist in revising advertising texts. "
    "Revise the given three posts based on the provided feedback while maintaining the social media style."
)
marketing_revision_system_message = SystemMessage(content=marketing_revision_prefix)
marketing_revision_agent = create_react_agent(
    model="gpt-3.5-turbo-1106",
    tools=[]
)

def marketing_content_agent_node(state: dict) -> dict:
    message = (
        f"User request: {state['question']}\n"
        "Generate three social media posts with an authentic and creative tone."
    )
    output = marketing_content_agent.invoke({
        "messages": [HumanMessage(content=message)]
    })
    posts = [post.strip() for post in output['messages'][-1].content.split("\n") if post.strip()]
    if len(posts) < 3:
        posts = posts + [""] * (3 - len(posts))
    return {"marketing_posts": posts}

def marketing_revision_agent_node(state: dict) -> dict:
    message = (
        f"Original posts:\n1. {state['marketing_posts'][0]}\n2. {state['marketing_posts'][1]}\n3. {state['marketing_posts'][2]}\n\n"
        f"User feedback: {state.get('revision_feedback', '')}\n\n"
        "Revise the posts incorporating the requested improvements."
    )
    output = marketing_revision_agent.invoke({
        "messages": [HumanMessage(content=message)]
    })
    revised_posts = [post.strip() for post in output['messages'][-1].content.split("\n") if post.strip()]
    if len(revised_posts) < 3:
        revised_posts = revised_posts + [""] * (3 - len(revised_posts))
    return {"final_posts": revised_posts}

# Build state graph and define flow
builder = StateGraph(MarketingState)
builder.add_node("MarketingContentAgent", marketing_content_agent_node)
builder.add_node("MarketingRevisionAgent", marketing_revision_agent_node)
builder.add_edge(START, "MarketingContentAgent")
builder.add_edge("MarketingContentAgent", "MarketingRevisionAgent")
builder.add_edge("MarketingRevisionAgent", END)
graph = builder.compile()

# Interactive conversational loop
print("=== Multi-Agent Marketing System ===")
print("Request a marketing post to receive three social media options.")
user_question = input("Enter your marketing request: ")
initial_state: MarketingState = {
    "question": user_question,
    "marketing_posts": [],
    "revision_feedback": None,
    "final_posts": None
}
state_after_content = graph.invoke(initial_state)
print("\n--- Generated Posts ---")
for idx, post in enumerate(state_after_content["marketing_posts"], start=1):
    print(f"Option {idx}: {post}")

feedback = input("\nRequest revisions? Type your feedback or press Enter to accept: ")
if feedback.strip():
    state_after_content["revision_feedback"] = feedback
    state_after_revision = graph.invoke(state_after_content)
    print("\n--- Revised Posts ---")
    for idx, post in enumerate(state_after_revision["final_posts"], start=1):
        print(f"Option {idx}: {post}")
else:
    print("\nYou accepted the initial posts.")

print("\n=== End of Process ===")
