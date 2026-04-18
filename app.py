from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from twilio.twiml.messaging_response import MessagingResponse
from SQL_alchemy import db, Sessao, Compromisso
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@127.0.0.1:3306/lembra_eu_brasil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
        sessao = Sessao(telefone=telefone, estado=1)
        db.session.add(sessao)
        db.session.commit()
        resp.message("Ola! Vou lhe ajudar a lembrar seus compromissos.\nQual o nome do compromisso?")
        return str(resp)
    
    if sessao.estado == 1:
        sessao.nome_temp = mensagem
        sessao.estado = 2
        db.session.commit()
        resp.message("Compromisso salvo! Informe a data 'DD/MM/AAAA':")
        return str(resp)
    
    elif sessao.estado == 2:
        # valida data
        try:
            data = datetime.strptime(mensagem, "%d/%m/%Y").date()
            sessao.data_temp = mensagem
            sessao.estado = 3
            db.session.commit()
            resp.message("Data salva! Informe a hora 'HH:MM':")
            return str(resp)
        except:
            resp.message("Data invalida! Use o formato DD/MM/AAAA:")
            return str(resp)
    elif sessao.estado == 3:
        # valida hora
        try:
            hora = datetime.strptime(mensagem, "%H:%M").time()
            data = datetime.strptime(sessao.data_temp, "%d/%m/%Y").date()
            
            # salva compromisso
            compromisso = Compromisso(
                telefone=telefone,
                nome=sessao.nome_temp,
                data=data,
                hora=hora,
                concluido=0
            )
            db.session.add(compromisso)
            
            sessao.estado = 1
            sessao.nome_temp = None
            sessao.data_temp = None
            db.session.commit()
            
            resp.message("Compromisso agendado com sucesso!")
            return str(resp)
        except:
            resp.message("Hora invalida! Use o formato HH:MM:")
            return str(resp)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)