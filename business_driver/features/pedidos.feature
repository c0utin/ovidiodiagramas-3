Feature: Gerenciamento de Pedidos no Sistema

  Scenario: Criar um pedido e verificar seu status
    Given um pedido é enviado
    When verifico o status do pedido
    Then o status deve ser "pendente"

  Scenario: Pedido expira após o timeout
    Given um pedido é enviado
    When espero mais que o tempo limite
    And verifico o status do pedido
    Then o status deve ser "timeout"

  Scenario: Pedido aceito pelo entregador antes do timeout
    Given um pedido é enviado
    When o entregador aceita o pedido dentro do tempo
    Then o status deve ser "aceito"
