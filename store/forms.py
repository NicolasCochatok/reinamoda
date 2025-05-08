from django import forms
from .models import ReviewRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
# ---------------------------------------------
# Formulario para cargar archivos Excel
# ---------------------------------------------
class ExcelUploadForm(forms.Form):
    archivo_excel = forms.FileField(label="Seleccionar archivo Excel")