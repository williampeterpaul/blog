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


def render_article_html(matter, body):
    builder = '<h1 style="margin-bottom:7px"> ' + matter['title'] + ' </h1>'
    builder += '<small style="float:left; color: #888">' + matter['date'] + '</small>'
    builder += '<small style="float:right; color: #888"><a href="/">See all posts</a></small>'
    builder += '<br>'
    builder += body

    return builder


def render_bibliography_html(bibliography):
    categories = []
    articles = []

    builder_categories = ''
    builder_articles = '<ul class="post-list">'

    for matter in bibliography:
        if matter['category'] not in categories:
            categories.append(matter['category'])
            builder_categories += '<a class="category" href="/test">' + matter['category'] + '</a>'

        articles.append([matter['title'], matter['date']])
        builder_articles += '<li>'
        builder_articles += '<span class="post-meta">' + matter['date'] + '</span>'
        builder_articles += '<h3 class="post-link"><a href="/test.html">' + matter['title'] + '</a></h3>'
        builder_articles += '</li>'


    return builder_categories + '<hr>' + builder_articles + '</ul>'


if __name__ == '__main__':
    project = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(project, 'build')

    style = open(os.path.join(project, 'style.css')).read()
    template = open(os.path.join(project, 'template.html')).read()

    if not os.path.exists(target):
        os.makedirs(target)

    bibliography = []

    for document in sys.argv[1:]:
        filename = os.path.split(document)[1]
        content = open(document).read()

        matter = parse_front_matter(content)
        body = parse_body(content)

        bibliography.append(matter)

        article = template.replace('</body>', render_article_html(matter, body) + '</body>')
        
        open(os.path.join(target, 'test.html'), 'w').write(article)

    index = template.replace(
        '</body>', render_bibliography_html(bibliography) + '</body>')

    open(os.path.join(target, 'index.html'), 'w').write(index)
    open(os.path.join(target, 'style.css'), 'w').write(style)
