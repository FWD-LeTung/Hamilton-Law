import re
from bs4 import BeautifulSoup
from langchain_core.documents import Document

DECOMPOSE_TAGS = ["script", "style", "head", "meta", "link", "noscript"]
UNWRAP_TAGS = ["font", "span", "b", "i", "u", "strong", "em", "sup", "sub"]

MIN_WORD = 20

def clean_html(raw_html: str) -> str:
    if not raw_html or not raw_html.strip():
        return ""
    soup = BeautifulSoup(raw_html, "lxml")
    
    for tag_name in DECOMPOSE_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    
    for tag_name in UNWRAP_TAGS:
        for tag in soup.find_all(tag_name):
            tag.unwrap()
    
    text = soup.get_text(separator="\n")
    return normalize_whitespace(text)

def word_count(text: str) -> int:
    return len(text.split())

def normalize_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()

def clean_documents(documents, min_word:int = MIN_WORD):
    n_total, n_dropped = 0, 0 
    
    for doc in documents:
        n_total += 1
        cleaned_text = clean_html(doc.page_content)
        wc = word_count(cleaned_text)

        if wc < min_word:
            n_dropped += 1
            continue

        new_metadata = {**doc.metadata, "word_count":wc}
        yield Document(page_content=cleaned_text, metadata=new_metadata)
    
    print(f"[Cleaner] Processed: {n_total}, Dropped (noise): {n_dropped}, "
          f"Kept: {n_total - n_dropped} documents")