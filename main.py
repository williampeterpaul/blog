#!/usr/bin/python3
import os
import sys
import re

def escape(content, quote=True):
    content = content.replace('&', '&amp;')
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    if quote:
        content = content.replace('"', '&quot;')
    return content


def parse_front_matter(content):
    matter = {}
    chunks = re.split('\n+', content)
    betweenSquareBracketsPattern = re.compile(r'(?<=\[).+?(?=\])')
    betweenRoundedBracketsPattern = re.compile(r'(?<=\().+?(?=\))')
    for chunk in chunks[:3]:
        squareBracketsMatch = re.search(betweenSquareBracketsPattern, chunk)
        roundedBracketsMatch = re.search(betweenRoundedBracketsPattern, chunk)
        # print(squareBracketsMatch.group())
        # print(roundedBracketsMatch.group())
        matter[squareBracketsMatch.group()] = roundedBracketsMatch.group()

    # print(matter)
    return matter


def parse_body(content):
    chunks = re.split('\n', content)
    return '\n'.join(chunks[4:])


def render_post(matter, body):
    pass


def render_table_of_contents(matter):
    pass


if __name__ == '__main__':
    builder = {'category': [], 'title': [], 'date': []}
    project = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(project, 'build')

    if not os.path.exists(target):
        os.makedirs(target)

    for document in sys.argv[1:]:
        filename = os.path.split(document)[1]
        content = open(document).read()

        matter = parse_front_matter(content)
        body = parse_body(content)

        if(matter['category'] not in builder['category']):
            builder['category'].append(matter['category'])
        if(matter['title'] not in builder['title']):
            builder['title'].append(matter['title'])
        if(matter['date'] not in builder['date']):
            builder['date'].append(matter['date'])

    content = open(os.path.join(project, 'template.html')).read()
    content = content.replace('</body>', '<h1>test</h1></body>')
    open(os.path.join(target, 'index.html'), 'w').write(content)
    print(builder)
    print(content)


