from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

TIMEOUT_PEDIDO = 10  # Timeout de 10 segundos
pedidos = {}

@app.route('/pedido', methods=['POST'])
def fazer_pedido():
    pedido_id = str(len(pedidos) + 1)
    pedidos[pedido_id] = "pendente"

    def timeout_handler(pedido_id):
        time.sleep(TIMEOUT_PEDIDO)
        if pedidos.get(pedido_id) == "pendente":
            pedidos[pedido_id] = "timeout"

    threading.Thread(target=timeout_handler, args=(pedido_id,)).start()
    return jsonify({"pedido_id": pedido_id, "status": "pendente"}), 202

@app.route('/pedido/<pedido_id>/status', methods=['GET'])
def verificar_status(pedido_id):
    status = pedidos.get(pedido_id, "desconhecido")
    return jsonify({"pedido_id": pedido_id, "status": status})

@app.route('/pedido/<pedido_id>/aceitar', methods=['POST'])
def aceitar_pedido(pedido_id):
    if pedido_id in pedidos and pedidos[pedido_id] == "pendente":
        pedidos[pedido_id] = "aceito"
        return jsonify({"pedido_id": pedido_id, "status": "aceito"}), 200
    return jsonify({"pedido_id": pedido_id, "status": "não encontrado ou expirado"}), 400

if __name__ == "__main__":
    app.run(port=5000)
