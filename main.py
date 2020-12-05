#!/usr/bin/python3
import os
import sys
import re

# Credit to Erik Vullings author of slimdown-js for the Regular Expressions https://github.com/erikvullings/slimdown-js
# This functionality has yet to be fleshed out - While parsing works on a basic level, it's far from meeting any formal markdown specifications
rules = [
    {
        'tag': 'header',
        'pattern': re.compile(r'(#+)(.*)'),
        'replace': lambda match: '<h{tag}>{content}</h{tag}>'.format(tag=len(match[0]), content=match[1])
    },
    {
        'tag': 'image',
        'pattern': re.compile(r'!\[([^\]]+)\]\(([^)]+)\)'),
        'replace': lambda match: '<img src="{source}" alt="{alternative}">'.format(source=match[1], alternative=match[0])
    },
    {
        'tag': 'link',
        'pattern': re.compile(r'[^!]\[([^\]]+)\]\(([^)]+)\)'),
        'replace': lambda match: '<a href="{href}">{content}</a>'.format(href=match[1], content=match[0])
    },
    {
        'tag': 'bold',
        'pattern': re.compile(r'(\*\*|__)(.*?)\1'),
        'replace': lambda match: '<strong>{content}</strong>'.format(content=match[1])
    },
    {
        'tag': 'emphasis',
        'pattern': re.compile(r'(\*|_)(.*?)\1'),
        'replace': lambda match: '<em>{content}</em>'.format(content=match[1])
    },
    {
        'tag': 'blockquote',
        'pattern': re.compile(r'\n(&gt;|\>)(.*)'),
        'replace': lambda match: '<blockquote>{content}</blockquote>'.format(content=match[1])
    },
    {
        'tag': 'horizontal rule',
        'pattern': re.compile(r'-{5,}'),
        'replace': lambda match: '<hr />'
    },
    {
        'tag': 'unordered list',
        'pattern': re.compile(r'\n(\*|\-|\+)(.*)'),
        'replace': lambda match: '<ul><li>{element}</li></ul>'.format(element=match[1])
    },
    {
        'tag': 'paragraph',
        'pattern': re.compile(r'[\n]{2,}'),
        'replace': lambda match: '<p></p>'
    }
]


def escape(value, quote=True):
    value = value.replace('&', '&amp;')
    value = value.replace('<', '&lt;')
    value = value.replace('>', '&gt;')
    if quote:
        value = value.replace('"', '&quot;')

    return value


def slugify(value):
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)

    return value


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

    return matter


def parse_body(content):
    chunks = re.split('\n', content)
    body = '\n'.join(chunks[4:])

    for rule in rules:
        for match in re.findall(rule['pattern'], body):
            # print("match", match)
            # print("rendered", rule['replace'](match))

            body = re.sub(rule['pattern'], rule['replace'](match), body, 1)

    return body


def parse_bibliography(bibliography):
    categories = []
    builder = ''

    for matter in bibliography:
        if matter['category'] not in categories:
            categories.append(matter['category'])

        builder += '<ul><li>{date} - <a href="{href}">{title}</a></li></ul>'.format(
            href=slugify(matter['title']) + '.html', title=matter['title'], date=matter['date'])

    return builder


if __name__ == '__main__':
    project = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(project, 'assets')
    target = os.path.join(project, 'build')

    template_style = open(os.path.join(assets, 'style.template.css')).read()
    template_index = open(os.path.join(assets, 'index.template.html')).read()
    template_article = open(os.path.join(
        assets, 'article.template.html')).read()

    if not os.path.exists(target):
        os.makedirs(target)

    os.system('cp {source} {destination}'.format(
        source=assets + '/*', destination=target))

    bibliography = []

    for document in sys.argv[1:]:
        filename = os.path.split(document)[1]
        content = open(document).read()

        matter = parse_front_matter(content)
        body = parse_body(content)
        bibliography.append(matter)

        article = template_article.format(
            content=body, date=matter['date'], title=matter['title'])
        open(os.path.join(target, slugify(
            matter['title']) + '.html'), 'w').write(article)

    body = parse_bibliography(bibliography)
    index = template_index.format(content=body)
    open(os.path.join(target, 'index.html'), 'w').write(index)
    open(os.path.join(target, 'style.css'), 'w').write(template_style)
