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
    elif "ftrack" in planilha:
        sheet="7891488269985668"
    #elif "fabrica" in planilha:
    #    sheet="4374521617639300"
    #elif "alcateia" in planilha:
    #    sheet="4103938677991300"


    #planilha de managers
    url = "https://api.smartsheet.com/2.0/sheets/"+sheet

    payload = ""
    headers = {
        'Authorization': "Bearer "+ smartsheet_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        #'Postman-Token': "6y1ult32nio7vth2d2nnwbnprx"
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
        msg = findpid(pid,data)
    elif local == "comstor":
        data = smartsheet("comstor")
        msg = findpid(pid,data)
    #elif local == "alcateia":
    #    data = smartsheet("alcateia")
    #    msg = findpid(pid,data)
    elif local == "ingram":
        data = smartsheet("ingram")
        msg = findpid(pid,data)
    #elif local == "fabrica":
    #    data = smartsheet("fabrica")
    #    msg = findpid(pid,data)
    elif local == "All":
        data = smartsheet("scansource")
        msg = findpid(pid,data)
        data = smartsheet("comstor")
        msg = msg + findpid(pid,data)
    #    data = smartsheet("alcateia")
    #    msg = msg + findpid(pid,data)
        data = smartsheet("ingram")
        msg = msg + findpid(pid,data)
    #    data = smartsheet("fabrica")
    #    msg = msg + findpid(pid,data)
    else:
        msg = "Local inválido. Locais válidos: Ingram, Scansource e Comstor."
        return msg


    #aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"

    return msg

def findpid(pid,data):
    # quantas linhas tem a planilha
    linhas = data['totalRowCount']
    #ultima vez que a planilha foi modificada
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
        #print (linha)
        #print(linha)
        # acessa a primeira celula da linha (parceiro)
        try:
            linha_pid=str(linha['cells'][0]['value'])
        except:
            linha_pid = "Sem_PID"
            print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
        # quantidade esta na columa 2 se for o reporta da fabrica ou columa 8 se for dos distribuidores

        #if local == "fabrica":
        #    try:
        #        qty_available = linha['cells'][1]['value']
        #    except:
        #        qty_available = 0
        #        print ("Verificar se o Smartsheet está com a coluna Quantity sem preencher")
        #else:
        try:
            qty_available = linha['cells'][7]['value']
        except:
            qty_available = 0
            print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
        #print (linha_pid)
        #print (linha_pid)
        # gera a linha formatada caso parceiro encontrado

        if pid in linha_pid.lower() and qty_available > 0:
            #print (local, qty_available)
            msg=msg+formata_pid(linha,local)
            #print (linha_pid + " contains given substring " +pid)
            #encontrado=encontrado+1
            #print ("Encontrado " + encontrado + " vezes.")
            #print (msg)
            encontrado=encontrado+1
            #print ("pid encontrado " + str(encontrado) + " vezes em estoque na " + str(local))
            #return msg


        count=count+1
        #print ("Loop count = " + str(count))
        #print(count)


        # devolva negativa caso nada encontrado
    #print (msg)

    if encontrado == 0:
        #print ("PID não encontrado em estoque na " + str(local))
        msg=("  \n" + "**Local:** " + str(local.upper()) + " **PID:** "+ pid + " não tem estoque " + "  \n")

    return msg


def ft(local):

    print("cheguei na funcao ft")
    
    if local == "scansource":
        data = smartsheet("ftrack")
        msg = findpid_ftrack(local,data)
    elif local == "comstor":
        data = smartsheet("ftrack")
        msg = findpid_ftrack(local,data)
    elif local == "ingram":
        data = smartsheet("ftrack")
        msg = findpid_ftrack(local,data)
    else:
        msg = "Local inválido. Locais válidos: Ingram, Scansource e Comstor."
        return msg
    
    if data=="erro":
        msg="Erro de acesso\n"

    return msg

def findpid_ftrack(local,data):
    # quantas linhas tem a planilha
    linhas = data['totalRowCount']
    #ultima vez que a planilha foi modificada
    data_modificacao = data['modifiedAt']

    #print (linhas)
    #print ("# de linhas na tabela: " + str(linhas))
    local == "ingram"
    #print (local)

    #print (nome_disti)
    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0

    msg=msg+("  \n**Local:** " + str(local.upper()) + " **Atualizado:** "+ data_modificacao.split("T")[0]+"  \n")

    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]
        #print (linha)
        #print(linha)
        # acessa a primeira celula da linha (parceiro)
        if local == "ingram":
            try:
                linha_pid=str(linha['cells'][0]['value'])
            except:
                linha_pid = "Sem_PID"
                print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
            try:
                qty_available = linha['cells'][1]['value']
            except:
                qty_available = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            #print (linha_pid)
            #print (linha_pid)
            # gera a linha formatada caso parceiro encontrado
        elif local == "comstor":
            try:
                linha_pid=str(linha['cells'][0]['value'])
            except:
                linha_pid = "Sem_PID"
                print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
            try:
                qty_available = linha['cells'][2]['value']
            except:
                qty_available = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            #print (linha_pid)
            #print (linha_pid)
            # gera a linha formatada caso parceiro encontrado
        elif local == "scansource":
            try:
                linha_pid=str(linha['cells'][0]['value'])
            except:
                linha_pid = "Sem_PID"
                print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
            try:
                qty_available = linha['cells'][3]['value']
            except:
                qty_available = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            #print (linha_pid)
            #print (linha_pid)
            # gera a linha formatada caso parceiro encontrado

        if linha_pid.lower() and qty_available > 0:
                #print (local, qty_available)
                msg=msg+formata_ftrack(linha,local)
                #print (linha_pid + " contains given substring " +pid)
                #encontrado=encontrado+1
                #print ("Encontrado " + encontrado + " vezes.")
                #print (msg)
                encontrado=encontrado+1
                #print ("pid encontrado " + str(encontrado) + " vezes em estoque na " + str(local))
                #return msg

        count=count+1
        #print ("Loop count = " + str(count))
        #print(count)


        # devolva negativa caso nada encontrado
    #print (msg)


    return msg

def smartft(pid,local):

    print("cheguei na funcao smartft")

    if pid=="":
        return

    if local == "scansource":
        data = smartsheet("ftrack")
        msg = findpid_ft(pid,data)
    elif local == "ingram":
        data = smartsheet("ftrack")
        msg = findpid_ft(pid,data)
    elif local == "comstor":
        data = smartsheet("ftrack")
        msg = findpid_ft(pid,data)
    elif local == "All":
        data = smartsheet("ftrack")
        msg = findpid_ft(pid,data)

    return msg

def findpid_ft(pid,data):

    print("cheguei na funcao findpid_ft")
    
    linhas = data['totalRowCount']
    data_modificacao = data['modifiedAt']

    local= ""
    linha_pid=""
    qty_available =0
    qty_available2 =0
    qty_available3=0

    msg=""
    count=0
    encontrado=0

    msg=msg+("\n**Local:** " + str(local.upper()) + " **Atualizado:** "+ data_modificacao.split("T")[0]+"  \n")

    while (count<linhas):
        
        linha=data['rows'][count]
        if local == "ingram":
            try:
                linha_pid=str(linha['cells'][0]['value'])
            except:
                linha_pid = "Sem_PID"
                print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
            try:
                qty_available = linha['cells'][1]['value']
            except:
                qty_available = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            #print (linha_pid)
            #print (linha_pid)
            # gera a linha formatada caso parceiro encontrado
        elif local == "comstor":
            try:
                linha_pid=str(linha['cells'][0]['value'])
            except:
                linha_pid = "Sem_PID"
                print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
            try:
                qty_available = linha['cells'][2]['value']
            except:
                qty_available = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            #print (linha_pid)
            #print (linha_pid)
            # gera a linha formatada caso parceiro encontrado
        elif local == "scansource":
            try:
                linha_pid=str(linha['cells'][0]['value'])
            except:
                linha_pid = "Sem_PID"
                print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
            try:
                qty_available = linha['cells'][3]['value']
            except:
                qty_available = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            #print (linha_pid)
        elif local == "All":
            try:
                linha_pid=str(linha['cells'][0]['value'])
            except:
                linha_pid = "Sem_PID"
                print ("Verificar se o Smartsheet está com a coluna de PID sem preencher")
            try:
                qty_available = linha['cells'][1]['value']
            except:
                qty_available = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            try:
                qty_available2 = linha['cells'][2]['value']
            except:
                qty_available2 = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            try:
                qty_available3 = linha['cells'][3]['value']
            except:
                qty_available3 = 0
                print ("Verificar se o Smartsheet com a coluna Quantity sem preencher")
            print (linha_pid)
            

            

        if linha_pid.lower() and qty_available or qty_available2 or qty_available3  > 0:
                #print (local, qty_available)
                msg=msg+formata_ft(linha,local)
                #print (linha_pid + " contains given substring " +pid)
                #encontrado=encontrado+1
                #print ("Encontrado " + encontrado + " vezes.")
                #print (msg)
                encontrado=encontrado+1
                #print ("pid encontrado " + str(encontrado) + " vezes em estoque na " + str(local))
                #return msg

        count=count+1
        #print ("Loop count = " + str(count))
        #print(count)


        # devolva negativa caso nada encontrado
    #print (msg)


    
    return msg

#########################################################
## FUNCOES de formatacao de texto para saida Webexteams

#########################################################

def formata_pid(dados, local):

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

    #Consulta original quanto tinhamos a fabrica também.
    #if local == "fabrica":

    #    try:
    #        pid=str(dados['cells'][0]['value'])
    #    except:
    #        pass
    #    try:
    #        qty_available=str(dados['cells'][1]['value']).split('.')[0]
    #    except:
    #        pass
    #    try:
    #        updated_by=str(dados['cells'][2]['value'])
    #    except:
    #        pass
    #    try:
    #        updated=str(dados['cells'][3]['value'])
    #    except:
    #        pass

    #    #monta a linha e imprime
    #    msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + "  \n")
    #    print (msg)
    #    return msg

    #Fazia um else para quando não era fabrica
    #else:

    try:
        pid=str(dados['cells'][0]['value'])
    except:
        pass
    try:
        qty_available=str(dados['cells'][7]['value']).split('.')[0]
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

    #monta a linha e imprime
    msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + "  \n")
    #print ("msg formata pid")
    print (msg)
    return msg
    #print ("msn formata pid depois de retornar o resultado")

    #return msg

def formata_ftrack(dados, local):
    msg=""
    pid=""
    qty_available=""
    updated=""

    if local == "ingram":
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][1]['value']).split('.')[0]
        except:
            pass
        try:
            updated=str(dados['cells'][5]['value'])
        except:
            pass
    elif local == "comstor":
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][2]['value']).split('.')[0]
        except:
            pass
        try:
            updated=str(dados['cells'][5]['value'])
        except:
            pass
    elif local == "scansource":
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][3]['value']).split('.')[0]
        except:
            pass
        try:
            updated=str(dados['cells'][5]['value'])
        except:
            pass
    
     #monta a linha e imprime
    msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + "  \n")
    #print ("msg formata pid")
    print (msg)
    return msg

def formata_ft(dados,local):
    msg=""
    pid=""
    qty_available=""
    qty_available2=""
    qty_available3=""
    updated=""

    if local == "ingram":
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][1]['value']).split('.')[0]
        except:
            pass
        try:
            updated=str(dados['cells'][5]['value'])
        except:
            pass
    elif local == "comstor":
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][2]['value']).split('.')[0]
        except:
            pass
        try:
            updated=str(dados['cells'][5]['value'])
        except:
            pass
    elif local == "scansource":
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][3]['value']).split('.')[0]
        except:
            pass
        try:
            updated=str(dados['cells'][5]['value'])
        except:
            pass
    elif local =="All":
        try:
            pid=str(dados['cells'][0]['value'])
        except:
            pass
        try:
            qty_available=str(dados['cells'][1]['value']).split('.')[0]
        except:
            pass
        try:
            qty_available2=str(dados['cells'][2]['value']).split('.')[0]
        except:
            pass
        try:
            qty_available3=str(dados['cells'][3]['value']).split('.')[0]
        except:
            pass
        try:
            updated=str(dados['cells'][5]['value'])
        except:
            pass
    
     #monta a linha e imprime
    msg=msg+(" **PID:** "+ pid + " **Qtd:** " + qty_available + "  \n")
    #print ("msg formata pid")
    print (msg)
    return msg

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
Consulta o estoque de um disti e da fabrica: estoque ***local*** ***pid_id*** - Exemplo: estoque Comstor 1815 \n

**Procura se o partnumber faz parte do programa FastTrack:** \n
___
Consultar o partnumbers participantes do FastTrack: ft  ***parceiro_cisco*** - Exemplo: ft comstor  \n

Valores válidos para local são: Scansource, Comstor e Ingram  \n
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
