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
        
        # Configurar el campo vivienda_tipo
        self.fields['vivienda_tipo'].choices = [('', 'Selecciona tipo de vivienda')] + list(SolicitudAdopcion.VIVIENDA_TIPO_CHOICES)
        
        # Configurar el campo patio
        self.fields['patio'].choices = [('', 'Selecciona una opción')] + list(SolicitudAdopcion.PATIO_CHOICES)
        
        # Asegurar que los campos son requeridos
        self.fields['vivienda_tipo'].required = True
        self.fields['patio'].required = True
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nombre_solicitante',
            'email',
            'telefono',
            'vivienda_tipo',
            'direccion',
            'patio',
            'experiencia_mascotas',
            'motivo_adopcion',
            'otros_animales',
            Submit('submit', 'Enviar Solicitud', css_class='btn btn-primary w-full')
        )

    def clean_patio(self):
        """Validar que el campo patio tenga un valor válido"""
        patio = self.cleaned_data.get('patio')
        valid_choices = [choice[0] for choice in SolicitudAdopcion.PATIO_CHOICES]
        
        if patio and patio not in valid_choices:
            raise forms.ValidationError('Por favor, selecciona una opción válida para el patio.')
        
        return patio

    def clean_vivienda_tipo(self):
        """Validar que el campo vivienda_tipo tenga un valor válido"""
        vivienda_tipo = self.cleaned_data.get('vivienda_tipo')
        valid_choices = [choice[0] for choice in SolicitudAdopcion.VIVIENDA_TIPO_CHOICES]
        
        if vivienda_tipo and vivienda_tipo not in valid_choices:
            raise forms.ValidationError('Por favor, selecciona un tipo de vivienda válido.')
        
        return vivienda_tipo

class FiltroPerrosForm(forms.Form):
    TAMANO_CHOICES = [('', 'Todos')] + Perro.TAMANO_CHOICES
    SEXO_CHOICES = [('', 'Todos')] + Perro.SEXO_CHOICES
    COLOR_CHOICES = [('', 'Todos')] + Perro.COLOR_CHOICES
    
    tamano = forms.ChoiceField(
        choices=TAMANO_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sexo = forms.ChoiceField(
        choices=SEXO_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    color = forms.ChoiceField(
        choices=COLOR_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    edad_min = forms.IntegerField(
        min_value=0, 
        max_value=20, 
        required=False, 
        label='Edad mínima',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1'})
    )
    edad_max = forms.IntegerField(
        min_value=0, 
        max_value=20, 
        required=False, 
        label='Edad máxima',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 5'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_action = ''
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
