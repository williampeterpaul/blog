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
        'resolve': lambda match: '<h{tag}>{content}</h{tag}>'.format(tag = len(match[0]), content = match[1])
    },
    {
        'tag': 'image', 
        'pattern': re.compile(r'!\[([^\]]+)\]\(([^)]+)\)'), 
        'resolve': lambda match: '<img src="{source}" alt="{alternative}">'.format(source = match[1], alternative = match[0])
    },
    {
        'tag': 'link', 
        'pattern': re.compile(r'[^!]\[([^\]]+)\]\(([^)]+)\)'), 
        'resolve': lambda match: '<a href="{href}">{content}</a>'.format(href = match[1], content = match[0])
    },
    {
        'tag': 'bold', 
        'pattern': re.compile(r'(\*\*|__)(.*?)\1'), 
        'resolve': lambda match: '<strong>{content}</strong>'.format(content = match[1])
    },
    {
        'tag': 'emphasis', 
        'pattern': re.compile(r'(\*|_)(.*?)\1'), 
        'resolve': lambda match: '<em>{content}</em>'.format(content = match[1])
    },
    {
        'tag': 'blockquote', 
        'pattern': re.compile(r'(&gt;|\>)(.*)'), 
        'resolve': lambda match: '<blockquote>{content}</blockquote>'.format(content = match[1])
    },
    {
        'tag': 'horizontal rule', 
        'pattern': re.compile(r'-{5,}'), 
        'resolve': lambda match: '<hr />'
    },
    {
        'tag': 'unordered list', 
        'pattern': re.compile(r'(\*|\-|\+)(.*)'), 
        'resolve': lambda match: '<ul><li>{element}</li></ul>'.format(element = match[1])
    }
]

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
    body = '\n'.join(chunks[4:])
    
    for rule in rules:
        for match in re.findall(rule['pattern'], body):
            print(match)
            print(rule['resolve'](match))

            print("\n")
            # body = body.replace(''.join(match), rule['resolve'](match))


    return body


def render_article_html(matter, body):
    builder = '<h1 style="margin-bottom:7px"> ' + matter['title'] + ' </h1>'
    builder += '<small>' + matter['date'] + '</small>'
    builder += '<small><a href="/">See all posts</a></small>'
    builder += '<br>'

    builder += body

    return builder


def render_bibliography_html(bibliography):
    categories = []
    articles = []

    builder_categories = ''
    builder_articles = '<ul>'

    for matter in bibliography:
        if matter['category'] not in categories:
            categories.append(matter['category'])
            builder_categories += '<a href="/test">' + matter['category'] + '</a>'

        if [matter['title'], matter['date']] not in articles:
            articles.append([matter['title'], matter['date']])
            builder_articles += '<li>'
            builder_articles += '<span>' + matter['date'] + '</span>'
            builder_articles += '<h3><a href="#">' + matter['title'] + '</a></h3>'
            builder_articles += '</li>'


    return builder_categories + '<hr>' + builder_articles + '</ul>'


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
            '</body>', render_article_html(matter, body) + '</body>')
        open(os.path.join(target, 'test.html'), 'w').write(article)

    index = template.replace(
        '</body>', render_bibliography_html(bibliography) + '</body>')
    open(os.path.join(target, 'index.html'), 'w').write(index)
    open(os.path.join(target, 'style.css'), 'w').write(style)

