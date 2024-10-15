from django import forms

class PeliculaForm(forms.Form):
    Titulo = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'})
    )
    Fecha = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    Nacionalidad = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nacionalidad'})
    )
    Productora = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Productora'})
    )
    
    # Campos para el director
    Director = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Director'})
    )
    Nacionalidad_Director = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nacionalidad Director'})
    )
    
    # Campos para el actor
    Actor_Nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Actor'})
    )
    Actor_Nacionalidad = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nacionalidad del Actor'})
    )
    Actor_Sexo = forms.ChoiceField(
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SocioForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=100)
    Dni = forms.CharField(label="DNI", max_length=20)
    Nombre = forms.CharField(label="Nombre", max_length=100)
    Direccion = forms.CharField(label="Dirección", max_length=255)
    Telefono = forms.CharField(label="Teléfono", max_length=15, required=False)
    Avalado_por = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        socios = kwargs.pop('socios', [])
        super().__init__(*args, **kwargs)
        self.fields['Avalado_por'].choices = socios