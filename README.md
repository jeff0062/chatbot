# 🤖 Chatbot Assistente de Agendamentos Híbrido

## 📌 Descrição

Este projeto consiste no desenvolvimento de um **chatbot assistente de agendamentos**, capaz de interagir com o usuário via WhatsApp para registrar compromissos e enviar lembretes automáticos.

A solução utiliza uma arquitetura híbrida, combinando **C++ (lógica)**, **Python (integração/API)** e **banco de dados SQL**.

---

## 🎯 Objetivo

Criar um sistema capaz de:

* 📅 Agendar compromissos via conversa natural
* 🔔 Enviar lembretes automáticos no horário correto
* 🤖 Simular um assistente pessoal inteligente

---

## 🏗️ Arquitetura do Sistema

```
Usuário (WhatsApp)
        ↓
Python (API / Webhook)
        ↓
C++ (Motor de lógica - Máquina de Estados)
        ↓
Banco de Dados (MySQL)
        ↓
Scheduler (Verificação de horários)
```

---

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza duas tabelas principais no MySQL:

### 📌 Tabela: compromissos

Responsável por armazenar os lembretes dos usuários.

```sql
CREATE TABLE compromissos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telefone VARCHAR(20),
    nome VARCHAR(100),
    data DATE,
    hora TIME,
    concluido TINYINT DEFAULT 0
);
```

### 📌 Tabela: sessoes

Responsável por controlar o estado da conversa de cada usuário.

```sql
CREATE TABLE sessoes (
    telefone VARCHAR(20) PRIMARY KEY,
    estado INT DEFAULT 1,
    nome_temp VARCHAR(100),
    data_temp VARCHAR(10),
    hora_temp VARCHAR(5)
);
```

💡 A tabela `sessoes` substitui o uso de estruturas em memória (como `map` no C++), permitindo que o sistema mantenha o estado da conversa de forma persistente e escalável.

Quando o Python recebe uma mensagem:

* consulta a tabela `sessoes`
* identifica em qual etapa o usuário está
* continua o fluxo da conversa corretamente

---

## 🎓 Nota Acadêmica

Embora existam tecnologias mais adequadas para a construção de chatbots, este projeto utiliza **C++ de forma intencional**, com foco em aprendizado profundo de lógica, controle de estado e manipulação de dados.

---

## 🚀 Status do Projeto

🔧 Em desenvolvimento
✔️ Cadastro de compromissos
✔️ Validação de data e hora
✔️ Estrutura inicial de lembretes

---

## 👨‍💻 Autor

Desenvolvido por:
 Jefferson Luiz Vieira dos Santos Junior 🚀
