from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la reseña'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu opinión...',
                'rows': 4
            }),
        }
