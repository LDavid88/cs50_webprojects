from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponse
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
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        content = html_converter(title)
        if content is not None:
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": content
            })
        else:
            search_list = []
            list = util.list_entries()
            for entry in list:
                if title.lower() in entry.lower():
                    search_list.append(entry)
            return render(request, "encyclopedia/search_list.html", {
                "search_list": search_list
            })


def new(request):
    if request.method == "POST":
        title = request.POST["add_name"].capitalize()
        text = request.POST["txt"]
        if title != "" and text != "" and title not in util.list_entries():
            util.save_entry(title, text)
            html = html_converter(title)
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": html
            })
        else:
            return HttpResponse("Encyclopedia already exists.")

    return render(request, "encyclopedia/new.html")
