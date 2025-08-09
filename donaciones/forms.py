from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Donacion, TipoDonacion

class DonacionForm(forms.ModelForm):
    tipo_donacion = forms.ModelChoiceField(
        queryset=TipoDonacion.objects.filter(activo=True),
        empty_label="Selecciona un tipo de donación",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Donacion
        fields = [
            'tipo_donacion', 'nombre_donante', 'email_donante', 
            'telefono_donante', 'cantidad', 'mensaje', 'anonimo'
        ]
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4}),
            'cantidad': forms.NumberInput(attrs={'step': '1', 'min': '1000'}),
        }
        labels = {
            'tipo_donacion': 'Tipo de donación',
            'nombre_donante': 'Nombre completo',
            'email_donante': 'Correo electrónico',
            'telefono_donante': 'Teléfono (opcional)',
            'cantidad': 'Monto ($ CLP)',
            'mensaje': 'Mensaje (opcional)',
            'anonimo': 'Donación anónima',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'tipo_donacion',
            Row(
                Column('nombre_donante', css_class='form-group col-md-6 mb-3'),
                Column('email_donante', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('telefono_donante', css_class='form-group col-md-6 mb-3'),
                Column('cantidad', css_class='form-group col-md-6 mb-3'),
            ),
            'mensaje',
            'anonimo',
            Submit('submit', 'Realizar Donación', css_class='btn btn-success btn-lg')
        )
