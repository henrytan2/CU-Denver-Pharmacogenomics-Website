from django.views import generic
from mysite.business.alderaan import Alderaan

class IndexView(generic.TemplateView):
    a = Alderaan()
    a.run_command("FASPR/FASPR -i FASPR/example/2mol.pdb -o output.pdb")
    template_name = 'index.html'


class ContactView(generic.TemplateView):
    template_name = 'contact.html'


class PeopleView(generic.TemplateView):
    template_name = 'people.html'
