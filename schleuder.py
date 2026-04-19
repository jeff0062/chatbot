from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
from datetime import datetime
from SQL_alchemy import db, Compromisso
import os
from dotenv import load_dotenv
load_dotenv("credenciais.env")

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_NUMBER = "whatsapp:+14155238886"  # numero sandbox do Twilio

def verificar_compromissos():
    from app import app
    with app.app_context():
        agora = datetime.now()
        
        compromissos = Compromisso.query.filter_by(concluido=0).all()
        
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        for c in compromissos:
            horario = datetime.combine(c.data, c.hora)
            diff = (horario - agora).total_seconds()
            
            if 0 <= diff <= 3600:# cada segundo
                client.messages.create(
                    body=f"🔔 Lembrete!\nVocê tem um compromisso hoje:\n📌 *{c.nome}*\n⏰ às {c.hora.strftime('%H:%M')}\n\nBoa sorte! 💪",
                    from_=TWILIO_NUMBER,
                    to=f"whatsapp:+{c.telefone}"
                )
                # marca como concluido
                c.concluido = 1
                db.session.commit()

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_compromissos, 'interval', minutes=5)
    scheduler.start()