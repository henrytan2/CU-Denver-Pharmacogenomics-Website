from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'index.html'


class ContactView(generic.TemplateView):
    template_name = 'contact.html'


class PeopleView(generic.TemplateView):
    template_name = 'people.html'
