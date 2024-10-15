from django import forms

class PeliculaForm(forms.Form):
    Titulo = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Fecha = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    Nacionalidad = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Productora = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Campos para el director
    Director = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Nacionalidad_Director = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Campos para el actor
    Actor_Nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Actor_Nacionalidad = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Actor_Sexo = forms.ChoiceField(
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_Titulo(self):
        titulo = self.cleaned_data.get('Titulo')
        return titulo.title()  # Capitaliza el título

    def clean_Nacionalidad(self):
        nacionalidad = self.cleaned_data.get('Nacionalidad')
        return nacionalidad.title()  # Capitaliza la nacionalidad

    def clean_Productora(self):
        productora = self.cleaned_data.get('Productora')
        return productora.title()  # Capitaliza la productora

    def clean_Director(self):
        director = self.cleaned_data.get('Director')
        return director.title()  # Capitaliza el nombre del director

    def clean_Nacionalidad_Director(self):
        nacionalidad_director = self.cleaned_data.get('Nacionalidad_Director')
        return nacionalidad_director.title()  # Capitaliza la nacionalidad del director

    def clean_Actor_Nombre(self):
        actor_nombre = self.cleaned_data.get('Actor_Nombre')
        return actor_nombre.title()  # Capitaliza el nombre del actor

    def clean_Actor_Nacionalidad(self):
        actor_nacionalidad = self.cleaned_data.get('Actor_Nacionalidad')
        return actor_nacionalidad.title()  # Capitaliza la nacionalidad del actor

    
    

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
        
    def clean_Nombre(self):
        nombre = self.cleaned_data.get('Nombre')
        return nombre.title()