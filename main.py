from config import * 
from webexteams_console_tools import webexconsole
from webexteams import *
from logica import logica
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json 
import os

# Testa existencia do Webhook. Caso negativo, cria
msg=ValidaWebhook(webhook_name,webhook_url)
# Imprime erro caso validacao do Webhook nao funcionou
if msg=="erro":
    print ("Erro de Webhook")

# Selecione (c) para teste e (w) para producao
formato = "w"


# http server
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

 	    # POST valida se o que chega sem dados via o Webhook
   	    # do POST e' que se chama a rotina de respnder ao usuario

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

	    # Conteudo
        content=json.loads(post_data.decode('utf-8'))

        # chama funcao para tratar POST
        trataPOST(content)

    


def trataPOST(content):

    # resposta as perguntas
    # trata mensagem quando nao e' gerada pelo bot. Se nao e' bot, entao usuario
    try:     
        if content['name']==webhook_name and content['data']['personEmail']!=botmail:
            # identifica id da mensagem
            msg_id=(content['data']['id'])
            # identifica dados da mensagem
            webextalk=getwebexMsg(msg_id)
            usermail=webextalk[2]
            mensagem=webextalk[0]
            sala=webextalk[1]

            # executa a logica
            msg=logica(mensagem,usermail)
        
            # Envia log de uso para outra sala
            #sala_log = getwebexRoomID(log_bot)
            #print (sala_log)
            #log_room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vODhhYzFiODAtYmRiZC0xMWU5LWI3NjEtN2Y4ZjU4YzU1MGFj"
            #print (log_room_id)
            #msg_log = "bot: Tem Estoque |" + "user:" + usermail + "| comando:" + mensagem
            #print (msg_log)
            #webexmsgRoomviaID(sala_log,msg_log)
            
            # Envia resposta na sala apropriada
            webexmsgRoomviaID(sala,msg)
            
            # Envia log de uso para outra sala
            #sala_log = getwebexRoomID(log_bot)
            #print (sala_log)
            #log_room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vODhhYzFiODAtYmRiZC0xMWU5LWI3NjEtN2Y4ZjU4YzU1MGFj"
            #print (log_room_id)
            #msg_log = "bot: Tem Estoque |" + "user:" + usermail + "| comando:" + mensagem
            #print (msg_log)
            #webexmsgRoomviaID(sala_log,msg_log)

    except:
            print("POST nao reconhecido")
            pass



def run(server_class=HTTPServer, handler_class=S, port=int(os.getenv('PORT',8080))):
        #Esta funcao roda efetivamente o servidor Web
        # PORT usa variavel PORT (tipico de servicos PaaS) ou porta 8080 caso nao definida (tipico para teste local http://localhost:8080)
        logging.basicConfig(level=logging.INFO)
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        logging.info('Starting httpd...\n')
        
        try:
     	    httpd.serve_forever()
        except KeyboardInterrupt:
       	    pass
        httpd.server_close()
        logging.info('Stopping httpd...\n')



if formato=="c":

    box=""

    # aviso
    print("exit para sair. help para comandos de usuario. help+ para comandos avançados")

    # a definicao do usermail (emai) e' importante para testar os filtros de usuario
    usermail=input("seu email>")


    while box !="exit":

        box=input(">")

        # testa console de ferramentas
        webexconsole(box)

        # logica para usuarios
        msg=logica(box,usermail)
        print (msg)

elif formato=='w':
    
    run()

else:

    print ("nenhum formato selecionado. Selecione (c) para teste e (w) para producao")
