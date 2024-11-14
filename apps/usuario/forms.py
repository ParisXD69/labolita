from django import forms
from .models import *



class jugada_form(forms.ModelForm):
    class Meta:
        model = jugada
        fields = ['numero_uno', 'numero_dos', 'numero_tres', 'numero_cuatro', 'numero_cinco', 'numero_seis']
        labels = {
            'numero_uno': 'Primer número 1-75',
            'numero_dos': 'Segundo número 1-75',
            'numero_tres': 'Tercer número 1-75',
            'numero_cuatro': 'Cuarto número 1-75',
            'numero_cinco': 'Quinto número 1-75',
            'numero_seis': 'Sexto número 1-25'
        }

        def clean_numero_uno(self):
            return self.validate_number(self.cleaned_data.get('numero_uno'))

        def clean_numero_dos(self):
            return self.validate_number(self.cleaned_data.get('numero_dos'))

        def clean_numero_tres(self):
            return self.validate_number(self.cleaned_data.get('numero_tres'))

        def clean_numero_cuatro(self):
            return self.validate_number(self.cleaned_data.get('numero_cuatro'))

        def clean_numero_cinco(self):
            return self.validate_number(self.cleaned_data.get('numero_cinco'))

        def clean_numero_seis(self):
            return self.validate_numberd(self.cleaned_data.get('numero_seis'))

        def validate_number(self, value):
            if value < 1 or value > 75:
                raise forms.ValidationError("El número debe estar entre 1 y 75.")
            return value

        def validate_numberd(self, value):
            if value < 1 or value > 25:
                raise forms.ValidationError("El número debe estar entre 1 y 25.")
            return value


class monto_form(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ['monto']
        labels = {'monto': 'Monto'}
        widgets = {
            'monto': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }


class premio_form(forms.ModelForm):
    class Meta:
        model = premio_ganador
        fields = '__all__'


class usuario_form(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'password1',
            'required': 'required',

        }
    ))
    password2 = forms.CharField(label='Confirmacion', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirme su contraseña',
            'id': 'password2',
            'required': 'required',

        }
    ))

    privilegios = forms.ChoiceField(
        choices=[
            ('Usuario','Usuario'),
            ('Administrador','Administrador'),
            ('Supremo','Supremo')
        ]
    )
    class Meta:
        model = usuario
        fields = ['username', 'nombre', 'apellidos', 'carnet_identidad', 'imagen', ]
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Usuario',
                }
            ),
            'nombre':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                    'required': 'required'
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellidos',
                    'required': 'required'
                }
            ),
            'carnet_identidad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Carnet Identidad',
                    'required': 'required'
                }
            ),

        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
