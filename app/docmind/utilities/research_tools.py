from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq

def research_pipeline(query: str) -> str:
    arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500))
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500))
    tavily = TavilySearch()

    tools = [arxiv, wiki, tavily]

    llm = ChatGroq(model="qwen/qwen3-32b")
    llm_with_tools = llm.bind_tools(tools=tools)

    result = llm_with_tools.invoke(f"Research the topic: {query}")
    return result