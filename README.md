# 🤖 Chatbot Assistente de Agendamentos Híbrido

## 📌 Descrição

Este projeto consiste no desenvolvimento de um **chatbot assistente de agendamentos**, capaz de interagir com o usuário via WhatsApp para registrar compromissos e enviar lembretes automáticos.

A solução utiliza uma arquitetura híbrida, combinando **C++ (monitor de alertas)**, **Python (conversa e integração)** e **banco de dados MySQL**.

---

## 🎯 Objetivo

Criar um sistema capaz de:

* 📅 Agendar compromissos via WhatsApp
* 🔔 Enviar lembretes automáticos no horário correto
* 🤖 Simular um assistente pessoal inteligente

---

## 🏗️ Arquitetura do Sistema
Usuário (WhatsApp)
↓
Twilio (Webhook)
↓
Python/Flask (Conversa + Máquina de Estados)
↓
MySQL (compromissos + sessoes)
↑
C++ (Monitor de alertas - roda separado)
verifica horários e dispara lembretes

---

## 🗄️ Estrutura do Banco de Dados

### 📌 Tabela: compromissos
Armazena os lembretes finalizados.

```sql
CREATE TABLE compromissos (
    id_compromisso INT AUTO_INCREMENT PRIMARY KEY,
    telefone VARCHAR(100) NOT NULL,
    nome VARCHAR(45) NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    concluido TINYINT DEFAULT 0
);
```

### 📌 Tabela: sessoes
Controla o estado da conversa de cada usuário.

```sql
CREATE TABLE sessoes (
    telefone VARCHAR(20) PRIMARY KEY,
    estado INT DEFAULT 1,
    nome_temp VARCHAR(100),
    data_temp VARCHAR(10),
    hora_temp VARCHAR(5)
);
```

💡 Quando o Python recebe uma mensagem:
* Consulta `sessoes` pelo telefone
* Identifica em qual etapa o usuário está
* Continua o fluxo corretamente
* Quando completo, salva em `compromissos` e reseta `sessoes`

O C++ lê `compromissos` periodicamente e verifica se chegou a hora de alertar.

---

## 🔧 Divisão de Responsabilidades

| Componente | Responsabilidade |
|------------|-----------------|
| Python/Flask | Recebe mensagens, gerencia estados, salva no banco |
| MySQL | Persiste compromissos e sessões |
| C++ | Monitor de horários e disparo de alertas |
| Twilio | Integração com WhatsApp |

---

## 🎓 Nota Acadêmica

Este projeto utiliza **C++ de forma intencional**, com foco em aprendizado de estruturas de dados, controle de estado, manipulação de arquivos e uso da biblioteca `<ctime>` para monitoramento de horários.

---

## 🚀 Status do Projeto

🔧 Em desenvolvimento  
✔️ Backend C++ (máquina de estados, validações, monitor)  
✔️ Banco de dados MySQL  
✔️ Models SQLAlchemy  
✔️ Webhook Flask/Twilio  
⏳ Integração ngrok  
⏳ Testes end-to-end  

---

## 👨‍💻 Autor

Desenvolvido por:
Jefferson Luiz Vieira dos Santos Junior 🚀
2026
