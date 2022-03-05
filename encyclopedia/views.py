from random import randint
from django.shortcuts import render
from django import forms

from . import util
from .templatetags import markdown_extras


class EntryForm(forms.Form):

    title = forms.CharField(label='Wiki Title', max_length=100)
    content = forms.CharField(widget=forms.Textarea, label="")



def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def display(request, title):
    return render(request, "encyclopedia/display.html", {
        "entry":util.get_entry(title)
    })


def entry_form(request):

    if request.method == 'POST':    

        form = EntryForm(request.POST)

        if form.is_valid():

            title = (form.cleaned_data['title'])
            content = ("# " + title + "\n\n" + form.cleaned_data['content'] + "\n").encode('ascii')
         
            util.save_entry(title, content)

        return render(request, "encyclopedia/display.html", {
        "entry": util.get_entry(title),
        })

    else:

        form = EntryForm()

        return render(request, "encyclopedia/entry_form.html", {
        "form": form
        })


def edit(request, title):

    content = util.get_entry(title).split("\n",2)[2]

    form = EntryForm()
    form['title'].initial = title
    form['content'].initial = content

    return render(request, "encyclopedia/edit_form.html", {
        'title': title,
        'form': form,
    })


def search(request):

    entries = util.list_entries()

    for indx in range(len(entries)):

        entries[indx] = entries[indx].upper()



    if request.method == 'GET':

        search_item = request.GET.get('q', None).upper()

        # Check if search item matches exactly as an entry
        if search_item in entries:

            return display(request, search_item)

        # Check if a substring of an entry matches return even empty
        else:

            entry_list = []

            for entry in entries:
                if search_item in entry:
                    entry_list.append(entry.capitalize())
            
            return render(request, 'encyclopedia/search_result.html', {
                'entries': entry_list,
            })

    # All other scenario redirect to the index page
    return index(request)


def random(request):

    entries = util.list_entries()
    total_entry = len(entries)

    # Generate a random number between 0 and total number of entry less one
    rand = randint(0, total_entry - 1)
    title = entries[rand]

    return render(request, "encyclopedia/display.html", {
        "entry":util.get_entry(title)
    })