from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import textwrap

def highlight_code_in_html(input_html):
    soup = BeautifulSoup(input_html, "html.parser")
    
    code_blocks = soup.find_all("code")

    for code in code_blocks:
        original_code = code.text
        lang = code.get("data-code-lang")
        
        if lang is None:
            continue 
        
        try:
            lexer = get_lexer_by_name(lang)
        except Exception:
            print(f"Warning: An invalid language \"{ lang }\" was passed in a code block.")
            continue

        original_code = textwrap.dedent(original_code)
        formatter = HtmlFormatter(nowrap=False, style="github-dark")
        highlighted_code = highlight(original_code, lexer, formatter)
        highlighted_code_html = BeautifulSoup(highlighted_code, "html.parser")

        code['class'] = list(set(code.get('class', []) + ['highlight']))
        code.clear()
        code.append(highlighted_code_html)

        parent_element = code.parent
        if parent_element.name == "pre":
            parent_element.clear()
            parent_element.append(code)

    return str(soup)
