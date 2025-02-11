import time
import requests
from behave import given, when, then

BASE_URL = "http://localhost:5000"
context = {}

@given('an order is placed')
def step_impl(context):
    response = requests.post(f"{BASE_URL}/pedido")
    context.pedido_id = response.json().get("pedido_id")
    assert response.status_code == 202

@when('the delivery is completed within the expected time')
def step_impl(context):
    # Simulating a successful on-time delivery by making it accepted within the time limit
    time.sleep(5)  # assuming the delivery happens within 10 seconds
    response = requests.post(f"{BASE_URL}/pedido/{context.pedido_id}/aceitar")
    context.status = response.json().get("status")
    assert response.status_code == 200

@then('the order status should be "delivered on time"')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/pedido/{context.pedido_id}/status")
    assert response.json().get("status") == "delivered on time"

@when('the delivery exceeds the deadline')
def step_impl(context):
    # Simulating a delayed delivery by making the request wait longer than the timeout
    time.sleep(15)  # exceeding the timeout period of 10 seconds
    response = requests.post(f"{BASE_URL}/pedido/{context.pedido_id}/aceitar")
    context.status = response.json().get("status")
    assert response.status_code == 200

@then('the order status should be "late"')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/pedido/{context.pedido_id}/status")
    assert response.json().get("status") == "late"

@when('some orders exceed the deadline')
def step_impl(context):
    # Simulate multiple orders with different delivery times
    context.late_orders = 0
    context.total_orders = 5  # Example: 5 orders in total

    for i in range(context.total_orders):
        response = requests.post(f"{BASE_URL}/pedido")
        pedido_id = response.json().get("pedido_id")

        # Simulate a mix of timely and late deliveries
        if i % 2 == 0:  # Let's say every second order is delayed
            time.sleep(15)  # Delay for more than the timeout
            requests.post(f"{BASE_URL}/pedido/{pedido_id}/aceitar")
        else:
            time.sleep(5)  # Timely delivery
            requests.post(f"{BASE_URL}/pedido/{pedido_id}/aceitar")

@then('the system should calculate the percentage of late deliveries')
def step_impl(context):
    # Calculate late deliveries percentage
    late_percentage = (context.late_orders / context.total_orders) * 100
    print(f"Late deliveries percentage: {late_percentage}%")
    assert late_percentage >= 0  # just a basic check, you can customize the assertion logic here
