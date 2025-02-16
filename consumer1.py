import pika
import re
import time

# Configuração de Rate Limiting
requests_per_ip = {}
RATE_LIMIT = 5  # Máximo de requisições por minuto

# Simulação de Autenticação via Token
VALID_TOKENS = {"seu-token-seguro"}

def sanitize_message(message):
    """Valida e sanitiza mensagens"""
    if not isinstance(message, str) or not message.strip():
        return None
    return re.sub(r"[<>;&]", "", message)

def rate_limit(client_ip):
    """Verifica se o IP atingiu o limite de requisições"""
    current_time = time.time()

    if client_ip not in requests_per_ip:
        requests_per_ip[client_ip] = []

    # Remove requisições mais antigas que 60s
    requests_per_ip[client_ip] = [t for t in requests_per_ip[client_ip] if current_time - t < 60]

    if len(requests_per_ip[client_ip]) >= RATE_LIMIT:
        print(f"🚨 Rate Limit: IP {client_ip} atingiu o limite de {RATE_LIMIT} requisições por minuto.")
        return False

    requests_per_ip[client_ip].append(current_time)
    return True

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Criar a fila (caso ainda não exista)
channel.queue_declare(queue='fila_teste')

# Função que processa mensagens recebidas com segurança
def callback(ch, method, properties, body):
    try:
        # Extrair headers com tratamento de erro
        headers = properties.headers if properties and properties.headers else {}
        token = headers.get("Authorization", None)
        client_ip = properties.app_id if properties and properties.app_id else "desconhecido"

        # Verificar autenticação
        if not token or token not in VALID_TOKENS:
            print(f"🚨 Acesso negado para IP {client_ip}: Token inválido ou ausente.")
            return

        # Aplicar rate limiting
        if not rate_limit(client_ip):
            return

        # Processar mensagem
        message = body.decode()
        sanitized_message = sanitize_message(message)

        if not sanitized_message:
            print("⚠️ Mensagem inválida recebida. Descartando...")
            return

        print(f"✅ [Mensagem recebida] IP: {client_ip} | Conteúdo: {sanitized_message}")

    except Exception as e:
        print(f"❌ Erro no processamento da mensagem: {e}")

# Configurar consumo com autenticação e rate limiting
channel.basic_consume(queue='fila_teste', on_message_callback=callback, auto_ack=True)

print(' [*] Aguardando mensagens com segurança. Para sair, pressione CTRL+C')
channel.start_consuming()
