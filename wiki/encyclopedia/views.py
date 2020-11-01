from django import forms
from django.shortcuts import render

from . import util

from markdown2 import Markdown

markdowner = Markdown()


class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))

class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                entry(request, item)

                if item.lower() in i.lower(): 
                    searched.append(i)
                    context = {'searched': searched, 'form': Search()}
            return render(request, "encyclopedia/search.html", context)

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "form":Search()})

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page) 

        context = {
            'page': page_converted,
            'title': title,
            'form': Search()
        }

        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found."})
       
def search(request,title):
    entries = util.list_entries()
    form = Search(request.POST)
    if form.is_valid():
        item = form.cleaned_data["item"]
        for i in entries:
            entry(request,item)
        else:
            return render(request, "encyclopedia/error.html", {"message": "The requested page was not found."})
    else:
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "form":Search()})

def create(request):
    if request.method == "POST":
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form": Search(), "message": "Page already exist"})
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)

                context = {
                    'form': Search(),
                    'page': page_converted,
                    'title': title
                }

                return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/create.html", {"form": Search(), "post": Post()})           

