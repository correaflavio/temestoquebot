import requests
import os
import json 

#########################################################
## FUNCOES SMARTSHEET

#########################################################

def smartsheet(planilha):

    # Este codigo abre uma determinada planilha no smartsheet e a retorna

    #token esta na variável de ambiente
    smartsheet_token=os.environ['SMART_TOKEN']

    # devolve erro caso variavel de ambiente do token nao encontrada
    if smartsheet_token=="":
        return "erro"

    if "scansource" in planilha:
        sheet="3981179922737028"
    elif "comstor" in planilha:
        sheet="6726686227097476"
    elif "ingram" in planilha:
        sheet="5371646502788"
    elif "fabrica" in planilha:
        sheet="4374521617639300"
    elif "alcateia" in planilha:
        sheet="4103938677991300"
    elif "ft_importado" in planilha:
        sheet="4245463219103620"
    elif "ft_brasil" in planilha:
        sheet="1149564892800900"
        



    #planilha de managers
    url = "https://api.smartsheet.com/2.0/sheets/"+sheet

    payload = ""
    headers = {
        'Authorization': "Bearer "+ smartsheet_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache",
#        'Postman-Token': "6y1ult32nio7vth2d2nnwbnprx"
        }

    
    response = requests.request("GET", url, data=payload, headers=headers)
    
    #pega conteudo pleno da planilha
    if response.status_code==200:
        json_res = json.loads(response.text)
        #print (json_res)
    else:
    # devolve erro caso nao consiga acessar smartsheet
        return "erro"

    return json_res


def log_bot_smartsheet(user,comando):

    # Este codigo registra em uma planilha do smartsheet o uso dos bots

    #token esta na variável de ambiente
    smartsheet_token=os.environ['SMART_TOKEN']
    
    smartsheet_bot_log_id = "6418465415292804"
    
    bot_name = "Tem Estoque"
    user_id = user
    command = comando
    

    #URL smartsheet para adicionar linhas 
    url = "https://api.smartsheet.com/2.0/sheets/"+ smartsheet_bot_log_id + "/rows"
    print (url)
    #payload com cada columa e o comando por coluna
    payload = {"toTop":True, "cells": [{"columnId": 1904224842868612, "value": bot_name}, {"columnId": 6407824470239108, "value": user_id}, {"columnId": 4156024656553860, "value": command}]}
    print (payload)
    
    headers = {
        'Authorization': "Bearer "+ smartsheet_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)
    
    #pega conteudo pleno da planilha
    if response.status_code==200:
        json_res = json.loads(response.text)
        #print (json_res)
    else:
    # devolve erro caso nao consiga acessar smartsheet
        return "erro"

    return json_res



#########################################################
## FUNCOES de Busca de informacoes

#########################################################


def smartpid(pid,local):
    
    # Procura por pids
    # 13.9.2019
    if pid=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    if local == "scansource":
        data = smartsheet("scansource")
        data_ft_brasil = smartsheet("ft_brasil")
        data_ft_importado = smartsheet("ft_importado")
        msg = findpid(pid,data, data_ft_brasil, data_ft_importado,local)
    elif local == "comstor":
        data = smartsheet("comstor")
        data_ft_brasil = smartsheet("ft_brasil")
        data_ft_importado = smartsheet("ft_importado")
        msg = findpid(pid,data, data_ft_brasil, data_ft_importado,local)
    elif local == "alcateia":
        data = smartsheet("alcateia")
        data_ft_brasil = smartsheet("ft_brasil")
        data_ft_importado = smartsheet("ft_importado")
        msg = findpid(pid,data, data_ft_brasil, data_ft_importado,local)
    elif local == "ingram":
        data = smartsheet("ingram")
        data_ft_brasil = smartsheet("ft_brasil")
        data_ft_importado = smartsheet("ft_importado")
        msg = findpid(pid,data, data_ft_brasil, data_ft_importado,local)
    elif local == "fabrica":
        data = smartsheet("fabrica")
        data_ft_brasil = smartsheet("ft_brasil")
        data_ft_importado = smartsheet("ft_importado")
        msg = findpid(pid,data, data_ft_brasil, data_ft_importado,local)
    elif local == "All":
        data_ft_brasil = smartsheet("ft_brasil")
        data_ft_importado = smartsheet("ft_importado")
        data = smartsheet("scansource")
        msg = findpid(pid,data, data_ft_brasil, data_ft_importado,local)
        data = smartsheet("comstor")
        msg = msg + findpid(pid,data, data_ft_brasil, data_ft_importado,local)
        data = smartsheet("alcateia")
        msg = msg + findpid(pid,data, data_ft_brasil, data_ft_importado,local)
        data = smartsheet("ingram")
        msg = msg + findpid(pid,data, data_ft_brasil, data_ft_importado,local)
        data = smartsheet("fabrica")
        msg = msg + findpid(pid,data, data_ft_brasil, data_ft_importado,local)
    else: 
        msg = "Local inválido. Locais válidos: Ingram, Scansource, Alcateia, Comstor e Fabrica"
        return msg
        

    #aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
    
    return msg


def findpid(pid, data, data_ft_brasil, data_ft_importado, local):
    # quantas linhas tem a planilha
    linhas = data['totalRowCount']
    data_modificacao = data['modifiedAt']

    #print (linhas)
    #print ("# de linhas na tabela: " + str(linhas))
    local = data['name'].lower()
    #print (local)
    
    #print (nome_disti)
    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    # formata nome do Distribuidir e a data de atualizacao da planilha (pega a data e elimina a hora)
    msg=msg+("  \n**Local:** " + str(local.upper()) + " **Atualizado:** "+ data_modificacao.split("T")[0]+"  \n")
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]
        #print(linha)
        # acessa a primeira celula da linha
        linha_pid=linha['cells'][0]['value']
        
        # quantidade esta na columa 2 se for o reporta da fabrica ou columa 8 se for dos distribuidores
        if local == "fabrica":
            qty_available = linha['cells'][1]['value']
        else:
            qty_available = linha['cells'][7]['value']
        #print (linha_pid)
        #print (linha_pid)         
        # gera a linha formatada caso parceiro encontrado
            
        if pid in linha_pid.lower() and qty_available > 0:
            #verificar se produto está no fast track
            print ("Cheguei no find ft dentro do find pid")
            msg = find_ft(pid, data_ft_brasil, data_ft_importado,local, linha)
            #print (local, qty_available)
            #msg=msg+formata_pid(linha,local,ft)
            #print (linha_pid + " contains given substring " +pid)
            #encontrado=encontrado+1
            #print ("Encontrado " + encontrado + " vezes.")
            #print (msg)
            encontrado=encontrado+1
            #print ("Findpid Encontrado x " + str(encontrado) + " vezes.")
            #print ("pid encontrado " + str(encontrado) + " vezes em estoque na " + str(local))
            #return msg
                
        count=count+1
        #print ("Findpid count = " + str(count))
        
        
                
        # devolva negativa caso nada encontrado
    #print (msg)
    
    if encontrado == 0:
        #print ("PID não encontrado em estoque na " + str(local))
        msg=("  \n" + "**Local:** " + str(local.upper()) + " **PID:** "+ pid + " não tem estoque " + "  \n")

    return msg


def find_ft(pid, data_ft_brasil, data_ft_importado,local, linha):
    # quantas linhas tem a planilha
    print ("Pid: " + pid)
    linhas_ft_brasil = data_ft_brasil['totalRowCount']
    linhas_ft_importado = data_ft_importado['totalRowCount']
    print ("# de linhas na tabela ft brasil: " + str(linhas_ft_brasil))
    print ("# de linhas na tabela ft importado: " + str(linhas_ft_importado))
    
    msg=""
    count=0
    encontrado=0
    
    #verifica se esta na lista ft Brasil
    while (count<linhas_ft_brasil):

        # valida 1 linha por vez
        linha_ft=data_ft_brasil['rows'][count]
        #print (linha)
        #print ("Linha ft:")
        #print(linha_ft)                
        #print ("")

        # acessa a primeira celula da linha
        linha_pid_0=linha_ft['cells'][0]
        #print ("linha_pid_0:")
        #print (linha_pid_0)
        #print ("")
        #print ("linha_pid_0 type: ")
        #print (type(linha_pid_0))
        
        linha_pid=linha_ft['cells'][0]['value']
        print ("linha pid:")
        print ("")

        print ("Linha #" + str(count) + ":" + str(linha_pid))        
        print ("")
        
        #verifica se produto está no fast track    
        if pid in linha_pid.lower():
            ft = str(linha_ft['cells'][3]['value'])
            encontrado=encontrado+1
            print ("Find ft  Encontrado x " + str(encontrado) + " vezes.")
            print ("Pid " + str(pid) + " com ft: " + str(ft) + "%")
            #msg=msg+formata_pid(linha_ft,local,ft)
            msg=formata_pid(linha,local,ft)
            
        count=count+1
    
    """ 
    msg=""
    count=0
    encontrado=0
           
    #verifica se esta na lista ft de importados
    while (count<linhas_ft_importado):

        # valida 1 linha por vez
        linha=data_ft_importado['rows'][count]
        #print (linha)
        #print(linha)
        # acessa a primeira celula da linha
        linha_pid=linha['cells'][0]['value']
        print ("Linha #" + str(count) + ":" + linha_pid)        
        
        
        #verifica se produto está no fast track    
        if pid in linha_pid.lower():
            ft = linha['cells'][3]['value']
            encontrado=encontrado+1
            print ("Pid " + pid + " com ft: " + str(ft) + "%")
            count=count+1
 
    """
               
    
    if encontrado == 0:
        #print ("PID não encontrado em estoque na " + str(local))
        msg = None

    return msg



#########################################################
## FUNCOES de formatacao de texto para saida Webexteams

#########################################################

def formata_pid(dados, local, ft):

    print("dados = ")
    print(dados)
    print ("ft = ")
    print (ft)
    print (type(ft))
    #lista de pids
    #13.09.2019
    
    # zera variaveis
    #print ("cheguei na funcao formata_pid")
    #print(dados)
    #print(local)
    msg=""
    pid=""
    qty_available=""
    updated=""
    updated_by=""

    #print (dados)
    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    
    if local == "fabrica":

        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][1]['value']).rstrip(".0")
        except:
            pass
        try:
            updated_by=str(dados['cells'][2]['value'])
        except:
            pass
        try:
            updated=str(dados['cells'][3]['value'])
        except:
            pass
            
        #monta a linha e imprime. Se o PID tem fasttrack imprime a informação, caso contrário não.
        if ft == "" or ft == None:
            msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + "  \n")
        else: 
            msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + " **FastTrack:** " + ft + "%" + "  \n")
        print (msg)
        return msg
               
    else:
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][7]['value']).rstrip(".0")
        except:
            pass
        try:
            updated_by=str(dados['cells'][8]['value'])
        except:
            pass
        try:
            updated=str(dados['cells'][9]['value'])
        except:
            pass
        
        print ("ft = " + str(ft))    
        #monta a linha e imprime
        if ft == "" or ft == None:
            msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + "  \n")
        else: 
            msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + " **FastTrack:** " + ft + "%" + "  \n")
        #print ("msg formata pid")
        print (msg)
        return msg
        print ("msn formata pid depois de retornar o resultado")
        
    #return msg
    



#########################################################
## FUNCOES API Suporte Cisco

#########################################################

def ajuda():

    # Funcao ajuda deste bot
    msg="""
Forma de uso:  \n
**Procura se tem um partnumber em estoque:**  \n
___
Consulta o estoque de todos os distis e fabrica: estoque ***pid_id*** - Exemplo: estoque 9300 \n
Consulta o estoque de um disti e da fabrica: estoque ***local*** ***pid_id*** - Exemplo: estoque fabrica 1815 \n
Valores válidos para local são: Scansource, Comstor, Ingram, Alcateia e Fabrica  \n
"""
    
    return msg


def getCiscoApiToken():
    
    #Chama Cisco.com para gerar token para consultas. Retorna Token

    url = "https://cloudsso.cisco.com/as/token.oauth2"

    # Dados criados de apiconsole.cisco.com

    payload = "client_id=7t9s28h7t5337pwknwdesssv&grant_type=client_credentials&client_secret=7xtCggEKxGAYKs4UTHYaKUsD"
    headers = {
    'content-type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    'Postman-Token': "f073e0db-6167-49c7-5e7a-54f4590331ff"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    resposta=json.loads(response.text)
    token=resposta['access_token']

    return token

def CiscoApiHello (token):

    # chama Cisco API para testes
    url = "https://api.cisco.com/hello"

    headers = {
    'Authorization': "Bearer "+token,
    'Cache-Control': "no-cache",
    'Postman-Token': "9d6632a7-0d65-a22e-2274-3bac58526c7f"
    }

    response = requests.request("GET", url, headers=headers)

    return response.text

def SupportAPIHello():

    # Testa API Hello
    token=getCiscoApiToken()
    nova_resp=CiscoApiHello(token)
    return nova_resp
        
    

#########################################################
## FUNCOES TECHMAPPING CISCO BRASIL
## Funcoes abaixo nao mais utilizadas apos migracao da base para Smartsheet

#########################################################
        
def autorizauser(usermail):

    # Esta funcao devolve true ou false para validar se usermail e' valido
    # (se pode pedir comando ou nao)

    # primeiro checa se email e da Cisco
    email=usermail.split("@")
        
    # caso positivo devolve true ou false
    if email[1]=="cisco.com":
        resultado = True
    else:
        resultado = False
   
    return resultado
