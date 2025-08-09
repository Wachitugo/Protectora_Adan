from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import SolicitudAdopcion, Perro

class SolicitudAdopcionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = [
            'nombre_solicitante', 'email', 'telefono', 'direccion',
            'experiencia_mascotas', 'motivo_adopcion', 'vivienda_tipo',
            'patio', 'otros_animales'
        ]
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'experiencia_mascotas': forms.Textarea(attrs={'rows': 4}),
            'motivo_adopcion': forms.Textarea(attrs={'rows': 4}),
            'otros_animales': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'nombre_solicitante': 'Nombre completo',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección completa',
            'experiencia_mascotas': 'Experiencia previa con mascotas',
            'motivo_adopcion': '¿Por qué quieres adoptar?',
            'vivienda_tipo': 'Tipo de vivienda',
            'patio': '¿Tienes patio?',
            'otros_animales': 'Otros animales en casa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre_solicitante', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-3'),
                Column('vivienda_tipo', css_class='form-group col-md-6 mb-3'),
            ),
            'direccion',
            'patio',
            'experiencia_mascotas',
            'motivo_adopcion',
            'otros_animales',
            Submit('submit', 'Enviar Solicitud', css_class='btn btn-primary')
        )

class FiltroPerrosForm(forms.Form):
    TAMANO_CHOICES = [('', 'Todos')] + Perro.TAMANO_CHOICES
    SEXO_CHOICES = [('', 'Todos')] + Perro.SEXO_CHOICES
    COLOR_CHOICES = [('', 'Todos')] + Perro.COLOR_CHOICES
    
    tamano = forms.ChoiceField(choices=TAMANO_CHOICES, required=False)
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, required=False)
    color = forms.ChoiceField(choices=COLOR_CHOICES, required=False)
    edad_min = forms.IntegerField(min_value=0, max_value=20, required=False, label='Edad mínima')
    edad_max = forms.IntegerField(min_value=0, max_value=20, required=False, label='Edad máxima')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Row(
                Column('tamano', css_class='form-group col-md-2 mb-3'),
                Column('sexo', css_class='form-group col-md-2 mb-3'),
                Column('color', css_class='form-group col-md-2 mb-3'),
                Column('edad_min', css_class='form-group col-md-2 mb-3'),
                Column('edad_max', css_class='form-group col-md-2 mb-3'),
                Column(Submit('submit', 'Filtrar', css_class='btn btn-primary'), css_class='form-group col-md-2 mb-3 d-grid'),
            ),
        )
