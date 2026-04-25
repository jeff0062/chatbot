import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from twilio.twiml.messaging_response import MessagingResponse
from SQL_alchemy import db, Sessao, Compromisso
from datetime import datetime
from scheduler import iniciar_scheduler

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

print(Sessao.__table__)
print(Compromisso.__table__)

with app.app_context():
    db.create_all()

@app.route("/webhook", methods=["POST"])
def webhook():
    telefone = request.form.get("From", "").strip()
    telefone = telefone.replace("whatsapp:", "").replace("+", "")

    if not telefone:
        return "Erro: From não enviado", 400

    mensagem = request.form.get("Body", "").strip()
    
    resp = MessagingResponse()
 
    print("FORM:", request.form)
    print("From:", request.form.get("From"))
    print("Body:", request.form.get("Body"))
    
    sessao = db.session.get(Sessao, telefone)

    if sessao is None:
        sessao = Sessao(telefone=telefone, estado=0)
        db.session.add(sessao)
        db.session.commit()
        resp.message("👋 Olá! Sou seu assistente de lembretes.\nVamos agendar seu compromisso ok?\n\n")
        return str(resp)
    
    if sessao.estado == 0:
        sessao.estado = 1
        db.session.commit()
        resp.message("📝 Qual o nome do compromisso?")
        return str(resp)

    elif sessao.estado == 1:
        sessao.nome_temp = mensagem
        sessao.estado = 2
        db.session.commit()
        resp.message("✅ Compromisso salvo!\n\n📅 Informe a data no formato *DD/MM/AAAA*:")
        return str(resp)
    
    elif sessao.estado == 2:
        # valida data
        try:
            data = datetime.strptime(mensagem, "%d/%m/%Y").date()
            sessao.data_temp = mensagem
            sessao.estado = 3
            db.session.commit()
            resp.message("✅ Data salva!\n\n⏰ Informe a hora no formato *HH:MM*:")
            return str(resp)
        except:
            resp.message("❌ Data inválida! Use o formato *DD/MM/AAAA*\nEx: 25/04/2026")
            return str(resp)
    
    elif sessao.estado == 3:
        try:
            hora = datetime.strptime(mensagem, "%H:%M").time()
            data = datetime.strptime(sessao.data_temp, "%d/%m/%Y").date()
        
            compromisso = Compromisso(
            telefone=telefone,
            nome=sessao.nome_temp,
            data=data,
            hora=hora,
            concluido=0
            )
            db.session.add(compromisso)
        
            sessao.estado = 4  # novo estado — aguardando decisão
            sessao.nome_temp = None
            sessao.data_temp = None
            db.session.commit()
        
            resp.message("✅ Compromisso agendado com sucesso!\n\nDeseja adicionar outro?\n1️⃣ - Sim\n2️⃣ - Encerrar")
            return str(resp)
        except:
            resp.message("❌ Hora inválida! Use o formato *HH:MM*\nEx: 14:30")
            return str(resp)

    elif sessao.estado == 4:
        if mensagem == "1":
            sessao.estado = 1
            db.session.commit()
            resp.message("📝 Qual o nome do próximo compromisso?")
        else:
            db.session.delete(sessao)
            db.session.commit()
            resp.message("Agradecemos o contato! Até logo! 👋")
            return str(resp)
        
    return str(resp)

iniciar_scheduler()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)