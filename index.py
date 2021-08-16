# -*- coding: utf-8 -*-
import bs4, requests, smtplib
import os
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client

load_dotenv()

def is_group_available_to_vaccine(site_url, target_group):
    getPage = requests.get(site_url)
    getPage.raise_for_status()

    schedule = bs4.BeautifulSoup(getPage.text, 'html.parser')
    groups = schedule.select('.form-group #comorbidity_id')

    length_target = len(target_group)
    available = False

    for group in groups:
        for i in range(len(group.text)):
            chunk = group.text[i:i+length_target].lower()
            if chunk == target_group:
                available = True
                print(chunk)
    
    return available

def send_email(google_app_password, recipient_email_list, sender_email, message_body):
    conn = smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
    conn.ehlo() # call this to start the connection
    conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
    
    conn.login(sender_email, google_app_password)
    conn.sendmail(sender_email, recipient_email_list, 'Subject: ALERTA: AGENDAMENTO DA VACINA!\n\n %s' % message_body)
    conn.quit()

    print('Notificacao enviada por e-mail para os seguintes destinatários:\n')
    for i in range(len(recipient_email_list)):
        print(recipient_email_list[i])
    print('')

def send_whatsapp_message(whatsapp_receiver_list, whatsapp_sender, message_body, whatsapp_twilio_sid, whatsapp_twilio_token):
    client = Client(whatsapp_twilio_sid, whatsapp_twilio_token)
    from_whatsapp_number = 'whatsapp:' + whatsapp_sender
    
    for whatsapp_receiver in whatsapp_receiver_list:
        to_whatsapp_number = 'whatsapp:' + whatsapp_receiver
        client.messages.create(body=message_body, 
            from_=from_whatsapp_number, 
            to=to_whatsapp_number)
    
    print('Notificacao enviada por whatsapp para os seguintes destinatários:\n')

    for i in range(len(whatsapp_receiver_list)):
        print(whatsapp_receiver_list[i])
    print('')

def run(site_url, google_app_password, recipient_email_list, sender_email, target_group, whatsapp_receiver_list, whatsapp_sender, whatsapp_twilio_id, whatsapp_twilio_token):
    available = is_group_available_to_vaccine(site_url, target_group)


    if available:
        message_body = 'Atencao!\n\nSua idade (%s) foi liberada para receber a vacina!\n\nPrepara a pff2, acesse %s e manda ver!\nVaxx Notifier V1.0' % (target_group, site_url)
        
        send_email(google_app_password, recipient_email_list, sender_email, message_body)
        send_whatsapp_message(whatsapp_receiver_list, whatsapp_sender, message_body, whatsapp_twilio_id, whatsapp_twilio_token)

        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print('script finalizado após disparar as notificações')
    else:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print('script finalizado sem disparar notificações')



GOOGLE_APP_PASSWORD = os.getenv('GOOGLE_APP_PASSWORD')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
WHATSAPP_TWILIO_ID = os.getenv('TWILIO_ACCOUNT_SID')
WHATSAPP_TWILIO_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
WHATSAPP_SENDER = os.getenv('WHATSAPP_SENDER')
WHATSAPP_RECEIVER_LIST = os.getenv('WHATSAPP_RECEIVER_LIST').split(',')
RECIPIENT_EMAIL_LIST = os.getenv('RECIPIENT_EMAIL_LIST').split(',')
TARGET_GROUP = 'população a partir de %s anos' % os.getenv('TARGET_AGE')
SITE_URL = 'https://coronavirus.palmas.to.gov.br/vacina/agendamento'

run(SITE_URL, GOOGLE_APP_PASSWORD, RECIPIENT_EMAIL_LIST, SENDER_EMAIL, TARGET_GROUP, WHATSAPP_RECEIVER_LIST, WHATSAPP_SENDER, WHATSAPP_TWILIO_ID, WHATSAPP_TWILIO_TOKEN )

