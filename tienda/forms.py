from django import forms

from django.contrib.auth.forms import UserCreationForm

# models.py
from .models import Usuario, Pedido

class RegistrarUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    rut = forms.CharField(required=True, label='Ingrese su rut')
    nombre = forms.CharField(required=True, label='Ingrese su Nombre')
    apellido = forms.CharField(required=True, label='Ingrese su Apellido')

    class Meta:
        model = Usuario
        fields = ['username','email', 'rut', 'nombre', 'apellido']

class PedidoForm(forms.ModelForm):
    direccion = forms.Textarea()
    formas_pago = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        choices=Pedido.CHOICES_PAGO, 
        required=True
    )
    class Meta:
        model = Pedido
        fields = ['direccion', 'formas_pago']

class CambiarEstadoPedidoForm(forms.ModelForm):
    estado_pedido = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        choices = Pedido.CHOICES_ESTADO,
        required=True
    )
    class Meta:
        model = Pedido
        fields = ['estado_pedido']

class TomarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion', 'estado_pedido']

    pedido_id = forms.IntegerField(widget=forms.HiddenInput)