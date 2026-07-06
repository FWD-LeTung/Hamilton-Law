import re
from bs4 import BeautifulSoup
from langchain_core.documents import Document

DECOMPOSE_TAGS = ["script", "style", "head", "meta", "link", "noscript"]
UNWRAP_TAGS = ["font", "span", "b", "i", "u", "strong", "em", "sup", "sub"]

MIN_WORD = 20

def clean_html(raw_html: str) -> str:
    pass

def word_count(text: str) -> int:
    pass

def normalize_whitespace(text: str) -> str:
    pass

def clean_documents(documents: Document, min_word:int = MIN_WORD) -> Document:
    pass