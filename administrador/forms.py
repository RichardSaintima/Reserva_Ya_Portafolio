from django import forms
from django.contrib.auth.models import User
from .models import DatosTransferencia,Pagos

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class DatosTransferenciaForm(forms.ModelForm):
    class Meta:
        model = DatosTransferencia
        fields=[
            'banco',
            'nombre',
            'numero_cuenta',
            'rut',
            'tipo_cuenta',
            'correo'
        ]
        widgets = {
            'tipo_cuenta': forms.Select(choices=DatosTransferencia.TIPO_CUENTA_CHOICES),
        }
    def clean_numero_cuenta(self):
        numero_cuenta= self.cleaned_data.get('numero_cuenta')
        if not (9 <= len(numero_cuenta) <= 12):
            raise forms.ValidationError("El número de cuenta debe tener entre 9 y 12 dígitos.")
        return numero_cuenta
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        
        # Verificar que el RUT contenga solo números
        if not rut.isdigit():
            raise forms.ValidationError("El RUT ingresado no es válido. Debe contener solo números.")
        
        # Obtener número y dígito verificador
        numero, verificador = rut[:-1], rut[-1].upper()
        
        # Calcular dígito verificador esperado usando el algoritmo del módulo 11
        suma = 0
        multiplicador = 2
        
        # Iterar sobre el número del RUT en orden inverso
        for d in reversed(numero):
            suma += int(d) * multiplicador
            multiplicador = multiplicador + 1 if multiplicador < 7 else 2
        
        # Obtener el resto
        resto = suma % 11
        
        # Calcular el dígito verificador esperado
        dv_esperado = 11 - resto if resto > 1 else 0
        
        # Comparar el dígito verificador calculado con el ingresado
        if dv_esperado != int(verificador):
            raise forms.ValidationError("El RUT ingresado no es válido.")
        
        return rut

class PagosForm(forms.ModelForm):
    class Meta:
        model= Pagos
        fields=['foto_comprobante']
        widgets = {
            'foto_comprobante': forms.FileInput(attrs={'accept': 'image/*'}),
        }
    def clean_foto_comprobante(self):
        foto_comprobante = self.cleaned_data.get('foto_comprobante')
        if not foto_comprobante:
            raise forms.ValidationError("Para poder cambiar el estado de 'No transferido' a 'Pagado' debe adjuntar la foto del comprobante.")
        return foto_comprobante