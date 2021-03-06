"""
From https://github.com/mayoff/python-markdown-mathjax
"""

import markdown

class MathJaxPattern(markdown.inlinepatterns.Pattern):

    def __init__(self):
        markdown.inlinepatterns.Pattern.__init__(self, r'(?<!\\)(\$\$?)(.+?)\2')

    def handleMatch(self, m):
        el = markdown.util.etree.Element("span")
        el.text = markdown.util.AtomicString(m.group(2) + m.group(3) + m.group(2))
        return el

class MathJaxExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        # Needs to come before escape matching because \ is pretty important in LaTeX
        md.inlinePatterns.add('mathjax', MathJaxPattern(), '<escape')

def makeExtension(configs=None):
    return MathJaxExtension(configs)
