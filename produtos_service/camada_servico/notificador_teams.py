import requests
import json

class NotificadorTeams:
    def __init__(self, webhook_url):
     
        self.webhook_url = webhook_url

    def enviar_mensagem(self, title, text, theme_color):
      
        mensagem = {
            "title": title,
            "text": text,
            "themeColor": theme_color
        }
        cabecalhos = {"Content-Type": "application/json"}
        resposta = requests.post(self.webhook_url, headers=cabecalhos, data=json.dumps(mensagem))
        if resposta.status_code == 200:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Erro ao enviar mensagem: {resposta.status_code} - {resposta.text}")
        return resposta



