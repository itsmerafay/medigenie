# # from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
# # from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
# # from langchain_tavily import TavilySearch
# # from langchain_groq import ChatGroq

# # def research_pipeline(query: str) -> str:
# #     arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500))
# #     wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500))
# #     tavily = TavilySearch()

# #     tools = [arxiv, wiki, tavily]

# #     llm = ChatGroq(model="qwen/qwen3-32b")
# #     llm_with_tools = llm.bind_tools(tools=tools)

# #     result = llm_with_tools.invoke(f"Research the topic: {query}")
# #     return result


# import os 
# from dotenv import load_dotenv
# from core.models import Session, Message

# load_dotenv()

# from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
# from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
# from langchain_tavily import TavilySearch
# from langchain_groq import ChatGroq
# from langgraph.graph import StateGraph, START, END
# from langgraph.prebuilt import ToolNode, tools_condition
# from typing_extensions import TypedDict
# from typing import Annotated
# from langgraph.graph.message import add_messages
# from langchain_core.messages import AnyMessage

# from research.utils import clean_markdown


# # class ResearchService:
# #     def __init__(self):
# #         self._initialize_tools_and_llm()

# #     def _initialize_tools_and_llm(self):
# #         arxiv_api = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
# #         wikipedia_api = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
        
# #         self.arxiv = ArxivQueryRun(api_wrapper=arxiv_api, description="Query Arxiv Paper")
# #         self.wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api, description="Query Wikipedia")
# #         self.tavily = TavilySearch()

# #         self.tools = [self.arxiv, self.wikipedia, self.tavily]
# #         self.llm = ChatGroq(model="qwen/qwen3-32b")

# #         self.llm_with_tools = self.llm.bind_tools(tools=self.tools)



# #     def _build_graph(self):
# #         class State(TypedDict):
# #             messages: Annotated[list[AnyMessage], add_messages]

# #         def tool_calling_llm(state: State):
# #             return {
# #                 "messages": [self.llm_with_tools.invoke(state["messages"])]
# #             }
        
# #         builder = StateGraph(State)
# #         builder.add_node("tool_calling_llm", tool_calling_llm)
# #         builder.add_node("tools", ToolNode(self.tools))
# #         builder.add_edge(START, "tool_calling_llm")
# #         builder.add_conditional_edges("tool_calling_llm", tools_condition)
# #         builder.add_edge("tools", "tool_calling_llm")

# #         return builder.compile()
    

# #     # def process_user_query(self, session: Session, query: str) -> str:
# #     #     graph = self._build_graph()
# #     #     result = graph.invoke({"messages": query})

# #     #     final_msg = None
# #     #     for msg in result["messages"]:
# #     #         if msg.type == "ai":
# #     #             final_msg = msg

# #     #     if not final_msg:
# #     #         final_msg = result["messages"][-1] 

# #     #     response_text = clean_markdown(final_msg.content.strip())

# #     #     Message.objects.create(
# #     #         session=session,
# #     #         content=response_text,
# #     #         role=Message.ROLECHOICES.ASSISTANT
# #     #     )

# #     #     return response_text



# #     def process_user_query(self, session: Session, query: str) -> str:
# #         graph = self._build_graph()

# #         for chunk in graph.stream({"messages": query}):
# #             yield chunk





# class ResearchService:
#     def __init__(self):
#         self._initialize_tools_and_llm()

#     def _initialize_tools_and_llm(self):
#         arxiv_api = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
#         wikipedia_api = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
        
#         self.arxiv = ArxivQueryRun(api_wrapper=arxiv_api, description="Query Arxiv Paper")
#         self.wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api, description="Query Wikipedia")
#         self.tavily = TavilySearch()

#         self.tools = [self.arxiv, self.wikipedia, self.tavily]
        
#         # Enable streaming in the LLM
#         self.llm = ChatGroq(
#             model="qwen/qwen3-32b",
#             streaming=True  # Enable streaming
#         )

#         self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

#     def _build_graph(self):
#         class State(TypedDict):
#             messages: Annotated[list[AnyMessage], add_messages]

#         def tool_calling_llm(state: State):
#             return {
#                 "messages": [self.llm_with_tools.invoke(state["messages"])]
#             }
        
#         builder = StateGraph(State)
#         builder.add_node("tool_calling_llm", tool_calling_llm)
#         builder.add_node("tools", ToolNode(self.tools))
#         builder.add_edge(START, "tool_calling_llm")
#         builder.add_conditional_edges("tool_calling_llm", tools_condition)
#         builder.add_edge("tools", "tool_calling_llm")

#         return builder.compile()
    
#     def process_user_query(self, session: Session, query: str):
#         """
#         Generator that yields chunks from the graph stream.
#         Each chunk has the format: {"node_name": {"messages": [...]}}
#         """
#         graph = self._build_graph()
        
#         # Stream mode will yield intermediate results from each node
#         for chunk in graph.stream(
#             {"messages": [{"role": "user", "content": query}]},
#             stream_mode="values"  # Stream intermediate values
#         ):
#             yield chunk


import os 
from dotenv import load_dotenv
from core.models import Session, Message

load_dotenv()

from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, AIMessageChunk


class ResearchService:
    def __init__(self):
        self._initialize_tools_and_llm()

    def _initialize_tools_and_llm(self):
        arxiv_api = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
        wikipedia_api = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
        
        self.arxiv = ArxivQueryRun(api_wrapper=arxiv_api, description="Query Arxiv Paper")
        self.wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api, description="Query Wikipedia")
        self.tavily = TavilySearch()

        self.tools = [self.arxiv, self.wikipedia, self.tavily]
        
        # Enable streaming in the LLM
        self.llm = ChatGroq(
            model="qwen/qwen3-32b",
            streaming=True
        )

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

    def _build_graph(self):
        class State(TypedDict):
            messages: Annotated[list[AnyMessage], add_messages]

        # Streaming node that yields tokens
        def tool_calling_llm_streaming(state: State):
            """This node will stream token by token"""
            response_chunks = []
            for chunk in self.llm_with_tools.stream(state["messages"]):
                response_chunks.append(chunk)
                # Yield each chunk for streaming
                yield {"chunk": chunk}
            
            # After streaming complete, return the full message
            # Combine all chunks into final message
            if response_chunks:
                full_message = response_chunks[0]
                for chunk in response_chunks[1:]:
                    full_message = full_message + chunk
                return {"messages": [full_message]}
            return {"messages": []}

        def tool_calling_llm(state: State):
            """Non-streaming fallback"""
            return {
                "messages": [self.llm_with_tools.invoke(state["messages"])]
            }
        
        builder = StateGraph(State)
        builder.add_node("tool_calling_llm", tool_calling_llm)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_edge(START, "tool_calling_llm")
        builder.add_conditional_edges("tool_calling_llm", tools_condition)
        builder.add_edge("tools", "tool_calling_llm")

        return builder.compile()
    
    def process_user_query_streaming(self, session: Session, query: str):
        """
        Generator that yields individual tokens from the LLM.
        This bypasses the graph for direct streaming.
        """
        graph = self._build_graph()
        
        # Get the initial state
        state = {"messages": [{"role": "user", "content": query}]}
        
        # Track if we're in a final response (no more tool calls)
        in_final_response = False
        
        for chunk in graph.stream(state, stream_mode="updates"):
            for node_name, node_update in chunk.items():
                messages = node_update.get("messages", [])
                
                if messages:
                    last_msg = messages[-1]
                    
                    # Check if this is tool_calling_llm node with AI message
                    if node_name == "tool_calling_llm":
                        # Check for tool calls
                        has_tool_calls = hasattr(last_msg, 'tool_calls') and last_msg.tool_calls
                        
                        if has_tool_calls:
                            # Tools will be called, send status
                            yield {"type": "status", "content": "[Searching with tools...]"}
                        elif hasattr(last_msg, 'content') and last_msg.content:
                            # This is the final answer, yield it
                            in_final_response = True
                            yield {"type": "answer", "content": last_msg.content}
    
    def process_user_query(self, session: Session, query: str):
        """
        Synchronous generator for node-level streaming.
        """
        graph = self._build_graph()
        
        for chunk in graph.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="values"
        ):
            yield chunk



