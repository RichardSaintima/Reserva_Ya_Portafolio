import hashlib
import hmac
from django.conf import settings
import requests
from django.urls import reverse

def sign_request(params):
    keys = sorted(params.keys())
    to_sign = ''.join(key + str(params[key]) for key in keys)
    signature = hmac.new(bytes(settings.FLOW_SECRET_SANDBOX, 'utf-8'), to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def make_request(url, params, method='GET'):
    signature = sign_request(params)
    params['s'] = signature

    if method == 'GET':
        response = requests.get(url, params=params)
    else:
        response = requests.post(url, data=params)
    return response.json()


def create_payment(request, id_pedido, monto, email):
    url = 'https://sandbox.flow.cl/api/payment/create'
    url_confirmation = 'https://www.youtube.com/watch?v=fZrhPotkl2M&t=609s'
    url_return = request.build_absolute_uri(reverse('plantillas:retorno_flow'))
    params = {
        'apiKey': settings.FLOW_KEY_SANDBOX,
        'commerceOrder': f"j{id_pedido}" ,
        'subject': 'Pago de pruebA',
        'currency': 'CLP',
        'amount': monto,
        'email': email,
        "urlConfirmation": url_confirmation,
        "urlReturn": url_return,
    }
    print("Parámetros para crear el pago:", params)

    response = make_request(url, params, method='POST')
    return response

def obtener_estado_pago(id_pedido):
    url = 'https://sandbox.flow.cl/api/payment/getStatus'  # URL del punto final para obtener el estado del pago
    params = {
        'apiKey': settings.FLOW_KEY_SANDBOX,  # Tu clave de API de Flow
        'commerceOrder': f"f{id_pedido}",      # El ID del pedido, con una "f" añadida al principio
    }
    print("Parámetros para obtener el estado del pago:", params)  # Imprimir los parámetros para depuración

    response = make_request(url, params, method='POST')  # Utilizar la función make_request para realizar la solicitud POST
    return response  # Devolver la respuesta de la API de Flow