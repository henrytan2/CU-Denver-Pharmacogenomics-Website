from django.views import generic
# from mysite.business.alderaan import Alderaan
import pickle5 as pickle

class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ContactView(generic.TemplateView):
    template_name = 'contact.html'


class PeopleView(generic.TemplateView):
    template_name = 'people.html'
