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
        'resolve': lambda match: '<h{tag}>{content}</h{tag}>'.format(tag=len(match[0]), content=match[1])
    },
    {
        'tag': 'image',
        'pattern': re.compile(r'!\[([^\]]+)\]\(([^)]+)\)'),
        'resolve': lambda match: '<img src="{source}" alt="{alternative}">'.format(source=match[1], alternative=match[0])
    },
    {
        'tag': 'link',
        'pattern': re.compile(r'[^!]\[([^\]]+)\]\(([^)]+)\)'),
        'resolve': lambda match: '<a href="{href}">{content}</a>'.format(href=match[1], content=match[0])
    },
    {
        'tag': 'bold',
        'pattern': re.compile(r'(\*\*|__)(.*?)\1'),
        'resolve': lambda match: '<strong>{content}</strong>'.format(content=match[1])
    },
    {
        'tag': 'emphasis',
        'pattern': re.compile(r'(\*|_)(.*?)\1'),
        'resolve': lambda match: '<em>{content}</em>'.format(content=match[1])
    },
    {
        'tag': 'blockquote',
        'pattern': re.compile(r'\n(&gt;|\>)(.*)'),
        'resolve': lambda match: '<blockquote>{content}</blockquote>'.format(content=match[1])
    },
    {
        'tag': 'horizontal rule',
        'pattern': re.compile(r'-{5,}'),
        'resolve': lambda match: '<hr />'
    },
    {
        'tag': 'unordered list',
        'pattern': re.compile(r'\n(\*|\-|\+)(.*)'),
        'resolve': lambda match: '<ul><li>{element}</li></ul>'.format(element=match[1])
    },
    {
        'tag': 'paragraph',
        'pattern': re.compile(r'\n([^\n]+)\n'),
        'resolve': lambda match: '<p>{content}</p>'.format(content=match)
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
            # print("rendered", rule['resolve'](match))

            body = re.sub(rule['pattern'], rule['resolve'](match), body, 1)

    return body


def render_article_html(matter, body):
    builder = '<small>' + matter['date'] + '</small>'
    builder += '<small style="float:right"><a href="index.html">See all posts</a></small>'
    builder += '<hr>'
    builder += '<h1 style="margin-bottom:7px"> ' + matter['title'] + ' </h1>'

    builder += body

    return builder


def render_bibliography_html(bibliography):
    categories = []
    category_builder = ''
    article_builder = ''

    for matter in bibliography:
        article_builder += '<ul>'
        article_builder += '<li>'
        article_builder += '<span>' + matter['date'] + '</span>'
        article_builder += '<h3>'
        article_builder += '<a href="{href}">'.format(href = slugify(matter['title']) + '.html')
        article_builder += matter['title']
        article_builder += '</a>'
        article_builder += '</h3>'
        article_builder += '</li>'
        article_builder += '</ul>'

        if matter['category'] not in categories:
            categories.append(matter['category'])
            category_builder += '<a href="{category}">'.format(category = slugify(matter['category']) + '.html')
            category_builder += matter['category']
            category_builder += '</a>'

    return category_builder + '<hr>' + article_builder


if __name__ == '__main__':
    project = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(project, 'assets')
    target = os.path.join(project, 'build')

    style = open(os.path.join(assets, 'style.css')).read()
    template = open(os.path.join(assets, 'template.html')).read()

    if not os.path.exists(target):
        os.makedirs(target)

    bibliography = []

    for document in sys.argv[1:]:
        filename = os.path.split(document)[1]
        content = open(document).read()

        matter = parse_front_matter(content)
        body = parse_body(content)
        bibliography.append(matter)

        article = template.replace(
            '</section>', render_article_html(matter, body) + '</section>')
        open(os.path.join(target, slugify(
            matter['title']) + '.html'), 'w').write(article)

    index = template.replace(
        '</section>', render_bibliography_html(bibliography) + '</section>')
    open(os.path.join(target, 'index.html'), 'w').write(index)
    open(os.path.join(target, 'style.css'), 'w').write(style)
