from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields= ['rut_empresa','nombre_empresa','razon_social','direccion_empresa','correo_electronico']
        labels = {
            'rut_empresa': 'Ingrese el Rut de la empresa',
            'nombre_empresa': 'Ingrese el nombre de la empresa',
            'razon_social': 'Ingrese la razon Social de la empresa',
            'direccion_empresa': 'Ingrese la dirección de su empresa',
            'correo_electronico': 'Ingrese el correo electronico'
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Establece los campos como obligatorios
            self.fields['rut_empresa'].required = True
            self.fields['nombre_empresa'].required = True
            self.fields['razon_social'].required = True
            self.fields['direccion_empresa'].required = True
            self.fields['correo_electronico'].required = True