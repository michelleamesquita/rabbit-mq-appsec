import pika

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Criar a fila (caso ainda não exista)
channel.queue_declare(queue='fila_teste')

# Configurar propriedades para incluir autenticação e IP
# properties = pika.BasicProperties(
#     headers={"Authorization": "seu-token-seguro"},  # Token correto
#     app_id="localhost"  # Simulação de um IP de origem
# )



# # Enviar mensagem
# message = "Mensagem segura para RabbitMQ"
# channel.basic_publish(exchange='', routing_key='fila_teste', body=message, properties=properties)

for i in range(7):
    message = f"Teste {i+1}"
    properties = pika.BasicProperties(
        headers={"Authorization": "seu-token-seguro"},  # Token correto
        app_id="localhost"  # Simulação de um IP local
    )
    channel.basic_publish(exchange='', routing_key='fila_teste', body=message, properties=properties)
    print(f" [✔] Enviado: {message}")

print(f" [✔] Mensagem enviada com segurança: {message}")

# Fechar conexão
connection.close()
