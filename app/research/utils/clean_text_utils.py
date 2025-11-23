import re

def clean_markdown(text: str) -> str:
    # Remove bold, italic, links, markdown symbols
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)    # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)        # italic
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text) # links
    text = text.replace("\\n", " ").replace("\n", " ")
    text = text.replace('\\"', '"')
    text = re.sub(r'\s+', ' ', text).strip()        # clean extra spaces
    return text
