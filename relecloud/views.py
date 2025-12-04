from django.shortcuts import render
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin  
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.db.models import Avg
from django.db.models import Count
from .forms import ReviewForm

# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def destinations(request):
    all_destinations = models.Destination.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-review_count', '-avg_rating')
    return render(request, 'destinations.html', {'destinations': all_destinations})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()

        # Obtener reseñas del destino
        reviews = destination.reviews.all()
        context['reviews'] = reviews

        # Calcular puntuación media
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = round(avg_rating, 1) if avg_rating else 0
        context['review_count'] = reviews.count()

        # Verificar si el usuario ya ha dejado una reseña
        if self.request.user.is_authenticated:
            user_review = reviews.filter(user=self.request.user).first()
            context['user_review'] = user_review
            context['can_review'] = not user_review
        else:
            context['can_review'] = False

        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cruise = self.get_object()

        # Obtener reseñas del crucero
        reviews = cruise.reviews.all()
        context['reviews'] = reviews

        # Calcular puntuación media
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = round(avg_rating, 1) if avg_rating else 0
        context['review_count'] = reviews.count()

        # Verificar si el usuario ya ha dejado una reseña
        if self.request.user.is_authenticated:
            user_review = reviews.filter(user=self.request.user).first()
            context['user_review'] = user_review
            context['can_review'] = not user_review
        else:
            context['can_review'] = False

        return context

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


class ReviewCreateDestination(LoginRequiredMixin, generic.CreateView):
    """Vista para crear reseña de un destino"""
    model = models.Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        # Obtener el destino
        self.destination = models.Destination.objects.get(pk=self.kwargs['destination_id'])
        # Verificar si el usuario ya tiene una reseña para este destino
        existing_review = self.destination.reviews.filter(user=request.user).exists()
        if existing_review:
            return HttpResponseForbidden("Ya has dejado una reseña para este destino")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.destination = self.destination
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('destination_detail', kwargs={'pk': self.destination.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destination'] = self.destination
        return context


class ReviewCreateCruise(LoginRequiredMixin, generic.CreateView):
    """Vista para crear reseña de un crucero"""
    model = models.Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        # Obtener el crucero
        self.cruise = models.Cruise.objects.get(pk=self.kwargs['cruise_id'])
        # Verificar si el usuario ya tiene una reseña para este crucero
        existing_review = self.cruise.reviews.filter(user=request.user).exists()
        if existing_review:
            return HttpResponseForbidden("Ya has dejado una reseña para este crucero")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.cruise = self.cruise
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cruise_detail', kwargs={'pk': self.cruise.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cruise'] = self.cruise
        return context
