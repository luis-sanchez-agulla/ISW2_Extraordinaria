from django.shortcuts import render
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin  
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': all_destinations})
# def destinations(request):
#     all_destinations = models.Destination.objects.all()
#     return render(request, 'destinations.html', { 'destinations': all_destinations})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class DestinationCreateView(generic.CreateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description']

class DestinationUpdateView(generic.UpdateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name', 'description']

class DestinationDeleteView(generic.DeleteView):
    model = models.Destination
    template_name = 'destination_confirm_delete.html'
    success_url = reverse_lazy('destinations')

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'
    
    def form_valid(self, form):
        # Save the model instance first (super handles saving and sets self.object)
        response = super().form_valid(form)

        # Prepare confirmation email to send to the requester
        subject = f"ReleCloud: informacion del mail recibida para {self.object.cruise}"
        body = (
            f"Hola {self.object.name},\n\n"
            f"Gracias por solicitar información sobre {self.object.cruise}. "
            "Hemos recibido su solicitud y nos pondremos en contacto con usted en breve.\n\n"
            "Sus notas:\n"
            f"{self.object.notes}\n\n"
            "Muchas gracias de parte de nuestro equipo"
        )
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else None)
        recipient_list = [self.object.email]

        try:
            send_mail(subject, body, from_email, recipient_list, fail_silently=False)
            messages.info(self.request, f"Email de confirmacion enviado a {self.object.email}.")
        except Exception as e:
            messages.error(self.request, f"No se pudo enviar el email de confirmacion: {e}")

        return response
