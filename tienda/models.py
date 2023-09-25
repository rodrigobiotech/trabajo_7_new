from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(User):

    rut = models.CharField()
    nombre = models.CharField()
    apellido = models.CharField()
    
    def __str__(self):
        return f'{self.nombre + " " + self.apellido}'
    
    class Meta:
        verbose_name_plural = 'Usuarios' 

class Pedido(models.Model):
    direccion = models.CharField()

    CHOICES_PAGO = [
        ("DEBITO", "Debito"),
        ("CREDITO", "Credito"),
        ("TRANSFERENCIA", "Transferencia"),
    ]

    formas_pago = models.CharField(choices=CHOICES_PAGO, default="DEBITO")
    
    CHOICES_ESTADO = [
        ("PENDIENTE", "Pendiente"),
        ("PREPARACION", "Preparacion"),
        ("ENVIADO", "Enviado"),
    ]

    estado_pedido = models.CharField(choices=CHOICES_ESTADO, default="PENDIENTE")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.usuario.username
    
    class Meta:
        verbose_name_plural = 'Pedidos'

class Producto(models.Model):
    nombre = models.CharField()
    precio = models.IntegerField()
    descripcion = models.CharField()
    sku = models.IntegerField()
    disponible = models.BooleanField()
    imagen = models.ImageField(upload_to='imagenes/', null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True )

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = 'Productos'



# class DetallePedido(models.Model):
#     pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     cantidad = models.IntegerField(default=0)

#     class Meta:
#         verbose_name_plural = 'Detalle Pedidos'

