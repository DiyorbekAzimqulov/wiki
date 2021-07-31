from django import forms


class EntryForm(forms.Form):
    title = forms.CharField(max_length=50, label="Title")
