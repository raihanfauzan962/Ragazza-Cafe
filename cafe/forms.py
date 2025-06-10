from django import forms
from .models import Review

class CheckoutForm(forms.Form):
    table_number = forms.CharField(max_length=10)
    payment_method = forms.ChoiceField(choices=[
        ('cash', 'Tunai'),
        ('non-cash', 'Non-Tunai'),
    ])
    note = forms.CharField(
        required=False,
        label="Catatan",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tambahkan catatan khusus (opsional)...'})
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
