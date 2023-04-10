from django.shortcuts import render
import markdown2
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from . import util
import random

TITLE = [""]
CONTENT = [""]


# default page
def index(request):
    entries = []
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})


# coonverter from .md to .html
def converter_md(title):
    file_to_convert = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if file_to_convert == None:
        return None
    else:
        return markdowner.convert(file_to_convert)


def entry(request, title):
    TITLE[0] = title
    converted_file = converter_md(title)
    if converted_file == None:
        return render(request, "encyclopedia/error_page.html")
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {"entry": converted_file, "title": title},
        )


# creating new website
class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def new_page(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            t = form.cleaned_data["title"]
            c = form.cleaned_data["content"]

        if t not in util.list_entries():
            util.save_entry(t, c)
            messages.success(request, "Your page is added successfully!")
        else:
            messages.info(request, "Title is alredy used")

    return render(
        request,
        "encyclopedia/new_page.html",
        {
            "form": NewTaskForm(),
        },
    )


# random page
def random_page(request):
    title = random.choice(util.list_entries())
    TITLE[0] = title
    converted_file = converter_md(title)
    if converted_file == None:
        return render(request, "encyclopedia/error_page.html")
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {"entry": converted_file, "title": title},
        )


# edit page
# class EditForm1(forms.Form):
#    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title"}))


def edit_page(request):
    if request.method == "POST":
        # title = request.POST.get("title")
        content = util.get_entry(TITLE[0])
        return render(
            request, "encyclopedia/edit.html", {"title": TITLE[0], "content": content}
        )
def save_changes(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(TITLE[0], content)
        to_html = converter_md(TITLE[0])
        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": title,
                "entry": to_html,
            },
        )


def search_engine(request):
    if request.method == "POST":
        to_search = request.POST["q"]
        to_html = converter_md(to_search)
        if to_html != None:
            return render(
                request,
                "encyclopedia/entry.html",
                {
                    "title": to_search,
                    "entry": to_html,
                },
            )
        else:
            posibilities = []
            entries = util.list_entries()
            for entry in entries:
                if to_search.lower() in entry.lower():
                    posibilities.append(entry)
            return render(
                request,
                "encyclopedia/search.html",
                {
                    "entries": posibilities,
                },
            )
