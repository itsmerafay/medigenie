from psychai.tools.therapist_tools import agent, SYSTEM_PROMPT


from psychai.tools.therapist_tools import agent, SYSTEM_PROMPT


def stream_therapist_response(user_text, username="User"):
    """
    Stream responses from the LangGraph agent with tool support.
    
    Args:
        user_text: The user's message
        username: The actual user's name for emergency situations
    """
    enhanced_prompt = f"""{SYSTEM_PROMPT}

    CRITICAL CONTEXT:
    - The user you are talking to is named: {username}
    - If you need to call emergency_call_tool, you MUST use this exact name: {username}
    - Do NOT use "Emily" or any other name for emergency calls
    """
        
    inputs = {
        "messages": [
            ("system", enhanced_prompt),
            ("user", user_text)
        ]
    }
    
    for msg, metadata in agent.stream(inputs, stream_mode="messages"):
        if hasattr(msg, 'content') and msg.content:
            content = msg.content
            
            if isinstance(content, str) and content.strip():
                yield content