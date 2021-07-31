from re import T
from django.shortcuts import render
from django.http import HttpResponseRedirect
import markdown
from .forms import EntryForm
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def detail(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/detail.html", 
        {
            "entry": markdown.markdown(entry),
            "title": title
        }
        )
    return render(request, 'encyclopedia/error.html', {})
    
def search(request):
    searched = request.GET.get('q', None)
    entry = util.get_entry(searched)
    if entry:
        return HttpResponseRedirect(redirect_to=f"wiki/{searched}")
    
    else:
        entries = util.list_entries()
        results = []
        for ent in entries:
            if searched in ent.lower():
                results.append(ent)
        return render(request, "encyclopedia/search_results.html", 
        {
            "results": results
        }
        )

def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = request.POST.get('body')
            is_saved = util.is_saved(title, content)
            if not is_saved:
                message = "Entry with that title already exists"
                return render(request, "encyclopedia/create.html", {
                    "message": message,
                    "form": form
                }
                )
            return HttpResponseRedirect(redirect_to=f'wiki/{title}')
        return render(request, "encyclopedia/create.html", {
            "form": form
        })
    return render(request, "encyclopedia/create.html", {
            "form": EntryForm()
        })
def edit(request, title):
    if request.method == "POST":
        title = title
        content = request.POST.get('content')
        util.save_entry(title=title, content=content)
        return HttpResponseRedirect(redirect_to=f"../{title}")
    content = util.get_entry(title)
    context = {
        "content": content
    }
    return render(request, "encyclopedia/edit.html", context)

def random_entry(request):
    entries = util.list_entries()
    random_n = random.randint(0, len(entries)-1)
    random_entry = entries[random_n]
    return HttpResponseRedirect(redirect_to=f"../wiki/{random_entry}")