import time
import requests
from behave import given, when, then

BASE_URL = "http://localhost:5000"
context = {}

@given('um pedido é enviado')
def step_impl(context):
    response = requests.post(f"{BASE_URL}/pedido")
    context.pedido_id = response.json().get("pedido_id")
    assert response.status_code == 202

@when('verifico o status do pedido')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/pedido/{context.pedido_id}/status")
    context.status = response.json().get("status")

@then('o status deve ser "pendente"')
def step_impl(context):
    assert context.status == "pendente"

@when('espero mais que o tempo limite')
def step_impl(context):
    time.sleep(11)

@then('o status deve ser "timeout"')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/pedido/{context.pedido_id}/status")
    assert response.json().get("status") == "timeout"

@when('o entregador aceita o pedido dentro do tempo')
def step_impl(context):
    response = requests.post(f"{BASE_URL}/pedido/{context.pedido_id}/aceitar")
    context.aceito_status = response.json().get("status")

@then('o status deve ser "aceito"')
def step_impl(context):
    assert context.aceito_status == "aceito"
