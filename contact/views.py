from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm
from .service import send_first


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'contact/tags/form.html'

    def form_valid(self, form):
        form.save()
        send_first(form.instance.email)
        return super().form_valid(form)