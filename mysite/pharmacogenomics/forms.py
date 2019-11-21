from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render


class DrugIDForm(forms.Form):
    drug_id = forms.CharField(label='Drug ID', max_length=100)
