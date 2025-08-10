from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Voluntario

class VoluntarioForm(forms.ModelForm):
    class Meta:
        model = Voluntario
        fields = [
            'nombre', 'apellidos', 'email', 'telefono', 'direccion',
            'fecha_nacimiento', 'experiencia', 'disponibilidad', 'motivacion'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'experiencia': forms.Textarea(attrs={'rows': 4}),
            'disponibilidad': forms.Textarea(attrs={'rows': 3}),
            'motivacion': forms.Textarea(attrs={'rows': 4}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'experiencia': 'Experiencia con animales',
            'disponibilidad': 'Disponibilidad horaria',
            'motivacion': '¿Por qué quieres ser voluntario?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nombre',
            'apellidos', 
            'email',
            'telefono',
            'fecha_nacimiento',
            'direccion',
            'experiencia',
            'disponibilidad',
            'motivacion',
            Submit('submit', 'Enviar Solicitud', css_class='btn btn-primary w-full')
        )
