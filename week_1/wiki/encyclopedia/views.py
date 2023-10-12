from django.shortcuts import render
from markdown2 import Markdown
from . import util


def html_converter(filename):
    markdowner = Markdown()
    entry = util.get_entry(filename)
    if entry is None:
        return None
    else:
        return markdowner.convert(entry)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    content = html_converter(title)
    if content is not None:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": content
        })

