# Multi-Agent Marketing System

## Overview
- **Purpose**: Generate creative, social media content and refine it based on user feedback using a multi-agent approach.
- **Approach**: Uses a state graph to coordinate the flow between agents for content creation and revision.

## Key Components
- **MarketingState**:
  - `question`: User's marketing request.
  - `marketing_posts`: Initially generated social media posts.
  - `revision_feedback`: Optional feedback for post revision.
  - `final_posts`: Revised social media posts after feedback.

- **Agents**:
  - **MarketingContentAgent**:  
    - Generates three initial social media posts with a creative and energetic tone.
  - **MarketingRevisionAgent**:  
    - Revises the generated posts based on provided feedback while keeping the authentic social media style.

## Architecture and Workflow
1. **User Input**:  
   - The user submits a marketing request.
2. **Content Generation**:  
   - **MarketingContentAgent** creates three creative social media posts.
3. **Feedback Collection**:  
   - The initial posts are shown to the user, and feedback is optionally provided.
4. **Post Revision**:  
   - **MarketingRevisionAgent** revises the posts in accordance with the feedback.
5. **Final Output**:  
   - The revised posts are presented as the final output.

## Technologies Used
- **Programming Language**: Python
- **Frameworks and Libraries**:
  - **LangGraph**: For building and managing the state graph.
  - **LangChain (create_react_agent)**: For agent creation and chat interactions.
  - **Pydantic and TypedDict**: For defining system state and ensuring type safety.

## Execution Flow Summary
- **Initialization**:
  - Define the marketing state and agent system messages.
  - Construct a state graph with nodes for content generation and revision.
- **Graph Processing**:
  - The graph receives the user’s marketing request, processes it through the MarketingContentAgent, and then optionally passes it through the MarketingRevisionAgent if feedback is provided.
- **Visualization**:
  - A Mermaid diagram image (`marketing_team_graph.png`) of the state graph is generated and saved.
- **User Interaction**:
  - A terminal-based REPL loop collects the marketing request and feedback, and displays initial and final social media posts.

## How to Run
1. **Install Dependencies**:
   - Ensure you have installed required packages such as `langgraph`, `langchain`, and `pydantic`.
2. **Execute the Script**:
   - Run the Python script.
   - Input your marketing request when prompted.
   - Provide revision feedback if desired.
3. **Review Outputs**:
   - The system will display the initial posts and, if feedback is given, the revised posts.
   - The generated state graph image will be saved as `marketing_team_graph.png`.
