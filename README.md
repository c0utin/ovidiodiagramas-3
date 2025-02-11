# Business Driver - Order Allocation Flow

## Overview

This project focuses on **reducing the average order allocation time** by implementing a timeout mechanism when a delivery driver does not accept the request or if an error occurs in the request process.

## Business Driver  

- **Objective**: Reduce the average order allocation time by **X%**.
- **Rule**: If the delivery driver does not accept the request within a defined timeout period, the request should be canceled or handled appropriately.

## System Diagram  

The following **DSL code** represents the interactions between the entities involved in the process:

```dsl
workspace "business_driver_fluxo_pedido" "Diagrama das partes envolvidas no processo" {

    !identifiers hierarchical

    model {
        empresa = softwareSystem "Empresa"
        rappi = softwareSystem "Rappi"
        entregador = softwareSystem "Entregador"

        empresa -> rappi "Faz requisição de pedido"
        rappi -> entregador "Repassa pedido"
        entregador -> rappi "Aceita ou recusa"
        rappi -> empresa "Confirma status do pedido"
    }

}
```

### **Diagram Explanation**
- **Empresa (Company)**: Sends the order request to **Rappi**.
- **Rappi**: Acts as an intermediary, passing the request to the **delivery driver**.
- **Entregador (Delivery Driver)**: Can either **accept** or **reject** the order.
- **Timeout Handling**: If the driver does not respond within the timeout period, **Rappi** notifies the company that the order request has expired.

## Gherkin & Testing Approach  

To ensure that the business rules are correctly implemented, we use **Gherkin** (with **Behave**) for testing.  

### **Role of Gherkin**
- Gherkin allows writing **human-readable** test scenarios that describe the expected system behavior.
- These scenarios are later **executed as automated tests** using the **Behave** framework.

### **Example Gherkin Test**
The following **Gherkin test** checks if an order request times out correctly when not accepted within the required time:

```gherkin
Feature: Order Management System

  Scenario: Order request times out if not accepted
    Given an order request is sent
    When the system waits beyond the timeout period
    Then the order status should be "timeout"
```

## Conclusion  

This project ensures that **order allocation** is optimized by reducing waiting time. The **timeout mechanism** helps prevent orders from being stuck indefinitely, improving efficiency. The **DSL diagram** provides a structured view of the process, and the **Gherkin tests** verify that business rules are properly enforced.
