# 🐇 RabbitMQ AppSec - Segurança no RabbitMQ

Este projeto demonstra como usar **RabbitMQ** com **Python** de forma segura, prevenindo ataques como **DoS (Denial of Service)**, **SQL Injection**, **XSS** e **Flooding** de mensagens. Ele inclui:
- **Produtor (Producer)**: Envia mensagens ao RabbitMQ.
- **Consumidor (Consumer)**: Processa mensagens da fila com segurança.
- **Rate Limiting**: Limita requisições por IP para evitar ataques DoS.
- **Autenticação com Token**: Apenas fontes autorizadas podem enviar mensagens.
- **Sanitização de Dados**: Remove comandos maliciosos de mensagens.

## 📌 1. Requisitos
- **Python 3.10+**
- **Docker** (para rodar o RabbitMQ)
- Pacotes Python: `pika`

Instale as dependências:
```sh
pip -r requirements.txt
```

---

## 🚀 2. Como Rodar o Projeto

### **1️⃣ Iniciar o RabbitMQ**
Se ainda não estiver rodando:
```sh
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

Acesse a interface web em [http://localhost:15672](http://localhost:15672). Usuário: `guest`, Senha: `guest`.

---

### **2️⃣ Rodar o Consumer (Receber Mensagens)**
Abra um terminal e execute:
```sh
python consumer.py
```
Saída esperada:
```
[*] Aguardando mensagens com segurança. Para sair, pressione CTRL+C
```

---

### **3️⃣ Rodar o Producer (Enviar Mensagens)**
Em outro terminal, rode:
```sh
python producer.py
```
Saída esperada:
```
[✔] Enviado: Teste 1
[✔] Enviado: Teste 2
[✔] Enviado: Teste 3
...
```
Se tudo estiver certo, o **consumer** irá exibir as mensagens recebidas.

---

## 📌 3. Código-Fonte

### **🔹 Producer (Envio de Mensagens) - `producer.py`**


### **🔹 Consumer (Receber e Processar Mensagens) - `consumer.py`**

---

## 📌 4. Testes de Segurança

### **🔹 Teste 1: Enviar Mensagens Maliciosas**
Rode o script abaixo (`producer_malicious.py`) para testar ataques:


Saída esperada no **consumer**:
```
✅ [Mensagem recebida] IP: localhost | Conteúdo: scriptalert('XSS')script
✅ [Mensagem recebida] IP: localhost | Conteúdo: ' OR '1'='1' --
✅ [Mensagem recebida] IP: localhost | Conteúdo: img src='x' onerror='alert("Hacked")'
```
Observe que os caracteres perigosos foram removidos!

---

## 📌 5. Conclusão
✅ **Rate Limiting impede spam de mensagens.**  
✅ **Token inválido bloqueia mensagens não autorizadas.**  
✅ **Sanitização protege contra XSS, SQL Injection e HTML Injection.**  
✅ **RabbitMQ agora está seguro contra ataques comuns.**  

Agora pode testar sem medo! 🚀🔥

