from django.shortcuts import render, redirect, get_object_or_404

# forms.py
from .forms import RegistrarUsuarioForm, PedidoForm, CambiarEstadoPedidoForm, TomarPedidoForm

# importar AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm

# importar logout, login, authenticate
from django.contrib.auth import authenticate, login, logout

# messages
from django.contrib import messages

# decoradores
from django.contrib.auth.decorators import login_required, user_passes_test

# models
from .models import Producto, Pedido

from django.db.models import Q


def inicio(request):
    return render(request, 'inicio.html')
    
def registro(request):
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.save()

            messages.success(request, f'Nueva cuenta creada: {user.username}')
            return redirect('inicio')
        else:
            for error in list(form.errors.values()):
                print(request, error)
    else:
        form = RegistrarUsuarioForm()

    return render(
        request=request,
        template_name='registro.html',
        context={"form":form}
    )

def custom_login(request):

    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user:
                
                login(request, user)
                messages.success(request, f'Bienvenido {user}')
                return redirect('inicio')
            
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = AuthenticationForm()

    return render(
        request=request,
        template_name='login.html',
        context={'form':form}
    )

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, f'Sesión finalizada con éxito.')
    return redirect ('inicio')

def ListaProductosView(request):
    productos = Producto.objects.filter(disponible=True, pedido__isnull=True)
    return render(request, 'productos.html', context={'productos':productos})

@login_required
def ListaPedidosView(request):
    if request.user.is_superuser or request.user.groups.filter(name='staff').exists():
        productos_con_pedido = Producto.objects.select_related('pedido__usuario').filter(pedido__isnull=False)
    else:
        productos_con_pedido = Producto.objects.select_related('pedido__usuario').filter(pedido__isnull=False, pedido__usuario=request.user)

    return render(request, 'pedidos.html', {'productos_con_pedido': productos_con_pedido})

@login_required
def agregar_producto(request, pk):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            producto = get_object_or_404(Producto, pk=pk)
            print(form)
            pedido = Pedido.objects.create(
                usuario=request.user,
                direccion = form.cleaned_data['direccion'],
                estado_pedido = 'PENDIENTE',
                )
            producto.pedido = pedido
            producto.disponible = False
            producto.save()
            
            return redirect('lista-pedidos')
        
    form = PedidoForm()
    return render(request, 'formularioPedido.html' , {'form': form } )

@login_required
def verPedido(request, pk):
    productos_con_pedido = Producto.objects.select_related('pedido__usuario').filter( pedido = pk, pedido__isnull=False)
    return render(request, 'verPedido.html', {'productos_con_pedido' : productos_con_pedido})

@login_required
def cambioEstadoPedido(request, pk):
    if request.method == 'POST':
        form = CambiarEstadoPedidoForm(request.POST)
        if form.is_valid():
            
            pedido = get_object_or_404(Pedido, pk=pk) 
            producto_asociado = Producto.objects.filter(pedido=pedido).first()
            pedido.estado_pedido = form.cleaned_data['estado_pedido']
            pedido.save()
            messages.success(request, f'Estado Pedido de Producto: {producto_asociado} actualizado.')
            
            return redirect('lista-pedidos')
        else:
            form = CambiarEstadoPedidoForm()
            messages.error(request, 'Ha ocurrido un error.')
        
    form = CambiarEstadoPedidoForm()
    if not request.user.groups.filter(name__in=['superusers','staff']).exists():
        messages.error(request, 'No tienes los permisos requeridos para realizar esta acción')
        return redirect('lista-pedidos')
    
    return render(request, 'formCambiarEstado.html' , {'form': form })

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='login-usuario')
def tomar_pedido(request):
    pedidos = Pedido.objects.exclude(usuario=request.user).filter(estado_pedido='PENDIENTE')
    if request.method == 'POST':
        form = TomarPedidoForm(request.POST)
        if form.is_valid():
            pedido_id = form.cleaned_data['pedido_id']
            pedido = get_object_or_404(Pedido, id=pedido_id)

            if pedido.estado_pedido == 'PENDIENTE':
                pedido.usuario = request.user
                pedido.estado_pedido = 'PREPARACION'
                pedido.save()
                messages.success(request, f'Pedido {pedido_id} tomado exitosamente.')
                return redirect('lista-pedidos')
    else:
        form = TomarPedidoForm()
    
    return render(request, 'tomar_pedido.html', {'form':form})
