from django import forms
from .models import PelucheFumo 


class FumoForm(forms.ModelForm):
    class Meta:
        model = PelucheFumo
        fields = [
            'nombre', 'categoria', 'fabricante', 'escala', 
            'descripcion', 'precio', 'stock', 'imagen', 'destacado', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Peluche Fumo Reimu Hakurei Ver. 1.5'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Gift / AmiAmi'}),
            'escala': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Non-Scale (~20cm)'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio del peluche Fumo debe ser superior a 0 CLP.")
        return precio