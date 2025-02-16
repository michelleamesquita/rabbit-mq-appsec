import pika

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Criar a fila (caso ainda não exista)
channel.queue_declare(queue='fila_teste')

# Lista de mensagens maliciosas para teste
malicious_messages = [
    "<script>alert('XSS')</script>",  # Teste de Cross-Site Scripting (XSS)
    "' OR '1'='1' --",  # Teste de SQL Injection
    "DROP TABLE users;",  # Teste de ataque SQL
    "<img src='x' onerror='alert(\"Hacked\")'>",  # Teste de injeção via HTML
    "Normal message but with & < > ;",  # Teste de sanitização
]

for i, message in enumerate(malicious_messages, start=1):
    properties = pika.BasicProperties(
        headers={"Authorization": "seu-token-seguro"},  # Token correto
        app_id="localhost"  # Identificação local
    )
    channel.basic_publish(exchange='', routing_key='fila_teste', body=message, properties=properties)
    print(f" [⚠] Enviado (Malicioso {i}): {message}")

# Fechar conexão
connection.close()
print(" [⚠] Todas as mensagens maliciosas foram enviadas.")
