#!/usr/bin/python3
import os, sys

def link(link, text=None):
    return f'<a href="{link}">' + (text or link) + '</a>'


def image(src, alt=None):
    return f'<img src="{src}" alt="{alt}" />'


def emphasis(text):
    return f'<em>{text}</em>'


def strong(text):
    return f'<strong>{text}</strong>'


def codespan(text):
    return f'<code>{text}</code>'


def inline_html(html):
    return html


def paragraph(text):
    return f'<p>{text}</p>\n'


def heading(text, level):
    tag = 'h' + level
    return f'<{tag}>{text}</{tag}>\n'


def newline():
    return ''


def line_break():
    return '<br />\n'


def horizontal_break():
    return '<hr />\n'


def block_text(text):
    return text


def block_code(code):
    return f'<pre><code>{code}</code></pre>\n'


def block_quote(text):
    return f'<blockquote>\n{text}</blockquote>\n'


def block_html(html):
    return f'<p>{html}</p>\n'


def block_error(html):
    return f'<div class="error">{html}</div>\n'


def unordered_list(text):
    return f'<ul>\n{text}</ul>\n'


def ordered_list(text):
    return f'<ol>\n{text}</ol>\n'


def list_item(text):
    return f'<li>{text}</li>\n'


def escape(s, quote=True):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
    return s


def parse_front_matter(matter):
    return {}


if __name__ == '__main__':
    for document in sys.argv[1:]:
        filename = os.path.split(document)[1]
        print(f'Processing file: {filename}')

        # Parse contents and front-matter
        contents = open(document).read()
        front_matter = parse_front_matter(contents)
        
        # Make build directory if it doesn't already exist
        path = "/c/Users/W/Documents/blog"
        target = os.path.join(path, '/build')

        print(target)

        if not os.path.exists(target):
            os.makedirs(target)
        
        print(contents)


