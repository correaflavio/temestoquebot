import requests
import os
import json 

#########################################################
## FUNCOES SMARTSHEET

#########################################################

def smartsheet(planilha):

    # Este codigo abre uma determinada planilha no smartsheet e a retorna

    #token esta na variável de ambiente
    #smartsheet_token=os.environ['SMART_TOKEN']
    smartsheet_token="j7txpag2g7iddvq0jtd3rahl6m"

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
    elif local == "alcateia":
        data = smartsheet("alcateia")
        msg = findpid(pid,data)
    elif local == "ingram":
        data = smartsheet("ingram")
        msg = findpid(pid,data)
    elif local == "fabrica":
        data = smartsheet("fabrica")
        msg = findpid(pid,data)
    elif local == "All":
        data = smartsheet("scansource")
        msg = findpid(pid,data)
        data = smartsheet("comstor")
        msg = msg + findpid(pid,data)
        data = smartsheet("alcateia")
        msg = msg + findpid(pid,data)
        data = smartsheet("ingram")
        msg = msg + findpid(pid,data)
        data = smartsheet("fabrica")
        msg = msg + findpid(pid,data)
    else: msg="local invalido"
        

    #aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
    
    return msg

def findpid(pid,data):
    # quantas linhas tem a planilha
    linhas = data['totalRowCount']
    #print (linhas)
    #print ("# de linhas na tabela: " + str(linhas))
    local = data['name'].lower()
    #print (local)
    
    #print (nome_disti)
    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]
        #print (linha)
        #print(linha)
        # acessa a primeira celula da linha (parceiro)
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
        msg="Pid: Nenhum resultado encontrado.  "

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
    '''
    if local == "fábrica":
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
            
        #monta a linha e imprime
        msg=msg+(str(local).upper() + " **PID:** "+ pid + " **Quantidade:** " + qty_available +  " unidade(s)." + " Atualizado em " + updated + " por " + updated_by + "  \n\n")
        #print (msg)
        return msg
            
     '''   
    #else:
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
            
        #monta a linha e imprime
    msg=msg+(str(local).upper() + " **PID:** "+ pid + " **Quantidade:** " + qty_available + " unidade(s)." + " Atualizado em " + updated + " por " + updated_by + "  \n\n")
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
**Procura se tem um partnumber (PID) em estoque:**  \n
___
Consulta o estoque de todos os distis e fabrica: pid ***pid_id***  \n
Consulta o estoque de um disti e da fabrica: pid ***local*** ***pid_id***  \n
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

def procurase(parceiro,arquitetura,especialidade):

    # Procura SE do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    # encerra se parceiro for nenhum (por enquanto)
    if parceiro=="":
        return

    # O 3o parametro desta funcao e' para entender especialidades do SE
    # caso tenha alguma, esta e' identificada, do contrario e' all (todas)
    hbox=especialidade.split(arquitetura)
    parametro=""
    
    if len(hbox)>1:
        parametro=hbox[1]
        especialidade=parametro.lstrip()
        especialidade=especialidade.rstrip()
    
    if especialidade=="":
        especialidade = "all"

    msg = ""
    count=0

    # Base de dados de acordo com a arquitetura definida

    if "sec" in arquitetura:
        filepath = "BASE_SECURITY.txt"
    if "dna" in arquitetura or "en" in arquitetura:
        filepath = "BASE_EN.txt"
    if "collab" in arquitetura:
        filepath = "BASE_COLLAB.txt"
    if "dc" in arquitetura or "data" in arquitetura:
        filepath = "BASE_DC.txt"

    # procura pessoa em parceiro especifico
    # No futuro incluir pesquisa em todos os parceiros caso parceiro = all (todos)

    if parceiro != "all":

        # loop de pesquisa e criacao da resposta 
        with open(filepath) as fp:  
            line = fp.readline()
            while line:
                texto=line.split(";")
                pname=texto[0]
                    
                # Caso encontrado o parceiro, investiga cada SE e competencias
                if parceiro in pname.lower():
                    if count == 0:
                        msg=("**Partner:**"+pname+"  \n")

                    sename=texto[1]
                    setel=texto[2]
                    semail=texto[3]
                    secomp=texto[4]
                                              
                    #identifica competencias
                    compet=""
                    for x in secomp.split(','):
                        if x !="":
                            compet = compet + "'" + x + "'"

                    # Seleciona se vai para impressao caso encontrado        

                    # Se nenhuma competencia declarada, entao vale todas
                    if especialidade == "all":
                        
                            msg=msg+("  \n**SE:** "+sename+": "+semail+" "+setel+"  \n")
                            if compet != "":
                                msg=msg+("**Competencies:**"+compet+"  \n")
                            count=count+1
                    
                    # Se competencia declarada, entao somente aquele SE que a possui
                    if especialidade != "all":
                        if compet != "" and especialidade in compet.lower():
                            msg=msg+("  \n**SE:** "+sename+": "+semail+" "+setel+"  \n")
                            msg=msg+("**Competencies:**"+compet+"  \n")
                            count=count+1

                  

                line = fp.readline()
                        
            # devolva negativa caso nada encontrado
            if count==0:
                msg="Nenhum resultado encontrado.  \n"

        return msg     


def procurapam(parceiro):

    # Procura PAM do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return


    msg = ""
    count=0

    # Procura o PAM do parceiro
    # Base de dados
    filepath = "basePAM.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                  
            # Caso encontrado cria resposta
            if parceiro in pname.lower():
                pcity=texto[1]
                ppam=texto[2]
                pmail=texto[3]
                pphone=texto[4]
    
                msg=msg+("**PAM do Parceiro:** "+pname+": "+ppam+" "+pmail+"@cisco.com "+pphone+" "+pcity+"  \n\n")
                count=count+1
                    
            line = fp.readline()
                    
        # devolva negativa caso nada encontrado
        if count==0:
            msg="PAM: Nenhum resultado encontrado.  "

    return msg     
        
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

def procuramanager(parceiro):

    # Procura Detalhes do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return

    msg=""
    count = 0

    
    # Procura os Managers do parceiro
    # Base de dados
    filepath = "SEM.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                
            # Caso encontrado cria resposta
            if parceiro in pname.lower():
                pcity=texto[1]
                pregion=texto[2]
                sem_title=texto[3]
                sem_name=texto[4]
                sem_mail=texto[5]
                sem_phone=texto[6]
                
                msg=msg+("**Manager:**"+sem_name+" **Title:**"+sem_title+" "+sem_phone+" "+sem_mail+"  \n")
                msg=msg+("**Region:**"+pregion+" **City:**"+pcity+"  \n\n")
                count = count + 1
                
            line = fp.readline()

    # tentativa de encontrar um SEM especifico caso a rotina acima nao retorne nada

    if count==0:    

        # loop de pesquisa  
        with open(filepath) as fp:  
            line = fp.readline()
            while line:
                texto=line.split(";")
                manager=texto[4]
                    
                # Caso encontrado cria resposta
                if parceiro in manager.lower():
                    pname=texto[0]
                    pcity=texto[1]
                    pregion=texto[2]
                    sem_title=texto[3]
                    sem_name=texto[4]
                    sem_mail=texto[5]
                    sem_phone=texto[6]
                    
                    msg=msg+("**Manager:**"+sem_name+" **Partner:**"+pname+" **Title:**"+sem_title+" "+sem_phone+" "+sem_mail+"  \n")
                    msg=msg+("**Region:**"+pregion+" "+pcity+"  \n\n")
                    count = count + 1
                    
                line = fp.readline()



        # devolva negativa caso nada encontrado
        if count==0:
            msg="Manager: Nenhum resultado encontrado.  \n"

    return msg   

def showtechmapping():

    # retorna lista de nome de parceiros do Tech Mapping

    msg = "\nLista de Parceiros Mapeados:\n"
    
    # Procura o PAM do parceiro
    # Base de dados
    filepath = "techmap.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                  
            msg=msg+pname+"\n"

            line = fp.readline()
                    
    return msg   
