from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

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

        formatter = HtmlFormatter(nowrap=True, style="github-dark")
        highlighted_code = highlight(original_code, lexer, formatter)
        highlighted_code_html = BeautifulSoup(highlighted_code, "html.parser")

        code['class'] = list(set(code.get('class', []) + ['highlight']))
        code.clear()
        code.append(highlighted_code_html)

        parent_element = code.parent
        if parent_element.name == "pre":
            parent_element.clear()
            parent_element.append(code)
    
    head_tag = soup.find('head')
    style_tag = soup.new_tag("style")
    style_tag.string = HtmlFormatter(style="github-dark").get_style_defs('.highlight')
    head_tag.insert(0, style_tag)

    return str(soup)
