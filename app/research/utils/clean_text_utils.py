import re

def clean_markdown(text: str) -> str:
    """
    Remove markdown formatting symbols from text while preserving content and spacing.
    Optimized for streaming chunks.
    
    Args:
        text: String containing markdown formatting
        
    Returns:
        Clean text without markdown symbols but with preserved spacing
    """
    # Remove headers (##, ###, etc.) - preserve newline after
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold (**text** or __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    
    # Remove italic (*text* or _text_) - be careful not to match ** 
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', text)
    text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'\1', text)
    
    # Remove inline code (`text`)
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    # Remove code blocks (```text```)
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # Remove strikethrough (~~text~~)
    text = re.sub(r'~~(.+?)~~', r'\1', text)
    
    # Remove links but keep text [text](url)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Remove bullet points (-, *, +) but preserve the space after
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    
    # Remove numbered lists (1., 2., etc.)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # Don't clean up extra whitespace - preserve original spacing
    # text = re.sub(r'\n{3,}', '\n\n', text)
    # text = text.strip()
    
    return text

