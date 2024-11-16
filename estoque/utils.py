from .models import Log

def registrar_log(usuario, acao):
    Log.objects.create(usuario=usuario, acao=acao)