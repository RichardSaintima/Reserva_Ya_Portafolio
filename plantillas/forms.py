from django import forms
from .models import Solicitud

from django import forms
from .models import Solicitud
from django.core.validators import RegexValidator

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields= ['rut_empresa', 'nombre_empresa', 'razon_social', 'direccion_empresa', 'correo_electronico']
        labels = {
            'rut_empresa': 'Ingrese el Rut de la empresa',
            'nombre_empresa': 'Ingrese el nombre de la empresa',
            'razon_social': 'Ingrese la razon Social de la empresa',
            'direccion_empresa': 'Ingrese la dirección de su empresa',
            'correo_electronico': 'Ingrese el correo electronico'
        }
        widgets = {
            'rut_empresa': forms.TextInput(attrs={'placeholder': '12.345.678-9'}),
            'nombre_empresa': forms.TextInput(attrs={'placeholder': 'Canchas San Beta'}),
            'razon_social': forms.TextInput(attrs={'placeholder': 'Razón Social de la empresa'}),
            'direccion_empresa': forms.TextInput(attrs={'placeholder': 'El Beta 1212'}),
            'correo_electronico': forms.EmailInput(attrs={'placeholder': 'correo@empresa.com'}),
        }

    rut_validator = RegexValidator(
        regex=r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$',
        message='Formato de RUT inválido. Debe ser del tipo 12.345.678-9'
    )
    
    rut_empresa = forms.CharField(
        label='Ingrese el Rut de la empresa',
        max_length=12,
        validators=[rut_validator],
        widget=forms.TextInput(attrs={'placeholder': '12.345.678-9'})
    )
    correo_electronico = forms.EmailField(
        label='Ingrese el correo electronico',
        widget=forms.EmailInput(attrs={'placeholder': 'correo@empresa.com'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establece los campos como obligatorios
        for field in self.fields:
            self.fields[field].required = True

    def clean_rut_empresa(self):
        rut = self.cleaned_data.get('rut_empresa')
        # Lógica de validación adicional para RUT si es necesario
        return rut

    def clean_correo_electronico(self):
        email = self.cleaned_data.get('correo_electronico')
        
        return email
