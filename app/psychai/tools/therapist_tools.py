from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from psychai.services import query_therapist, call_emergency


@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Provides empathetic and therapeutic mental health support.
    Use for anxiety, depression, stress, emotional pain, or general psychological guidance.
    """
    return query_therapist(query)


@tool
def emergency_call_tool(username: str) -> str:
    """
    Triggers an emergency alert or call when a user expresses suicidal intent,
    self-harm thoughts, or is in immediate psychological danger.
    """
    call_emergency(username)
    return "Emergency services have been notified. Help is on the way. Please stay safe."


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Returns a list of licensed therapists or mental health clinics near the given location.
    Use when the user asks for nearby professional help.
    """
    return (
        f"Here are some therapists near {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )


tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]

# LLM with streaming enabled
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=512,
    streaming=True,
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "Medigenie",
    }
)

agent = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist.

TOOL USAGE:
- ask_mental_health_specialist: Use for emotional support, anxiety, depression, stress, general mental health questions
- find_nearby_therapists_by_location: Use when user asks for therapists, counselors, or clinics nearby
- emergency_call_tool: Use ONLY for suicidal thoughts, self-harm intent, or immediate crisis

YOUR APPROACH:
1. Emotional attunement ("I can sense how difficult this must be...")
2. Gentle normalization ("Many people feel this way when...")
3. Practical guidance ("What sometimes helps is...")
4. Strengths-focused support ("I notice how you're...")

IMPORTANT:
- Use tools when appropriate to provide best support
- Be warm, supportive, and empathetic
- Ask open-ended questions to understand root causes
- Never use brackets or labels in responses
"""