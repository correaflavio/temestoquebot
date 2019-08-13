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

    if "sec" in planilha:
        sheet="1219329522984836"
    elif "dna" in planilha:
        sheet="835914437027716"
    elif "collab" in planilha:
        sheet="2994385685112708"
    elif "dc" in planilha:
        sheet="5992706112546692"
    elif "sem" in planilha:
        sheet="2210243842205572"
    elif "pam" in planilha:
        sheet="8872345856173956"
    elif "meraki" in planilha:
        sheet="6475499091322756"
    elif "4PS" in planilha:
        sheet="1400202272761732"
    elif "dap" in planilha:
        sheet="7330531516934020"
    elif "solution" in planilha:
        sheet="6200566423545732"
    elif "agenda" in planilha:
        sheet="7416587629160324"
    elif "pid" in planilha:
        sheet="3981179922737028"


    #planilha de managers
    url = "https://api.smartsheet.com/2.0/sheets/"+sheet

    payload = ""
    headers = {
        'Authorization': "Bearer "+ smartsheet_token,
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "6y1ult32nio7vth2d2nnwbnprx"
        }

    
    response = requests.request("GET", url, data=payload, headers=headers)
    
    #pega conteudo pleno da planilha
    if response.status_code==200:
        json_res = json.loads(response.text)
    else:
    # devolve erro caso nao consiga acessar smartsheet
        return "erro"

    return json_res


#########################################################
## FUNCOES de Busca de informacoes

#########################################################


def smartse(parceiro,arquitetura,especialidade):

    # Procura SE do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet(arquitetura)

    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg

    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    #leva conteudo da planilha para variavel sheet
    #sheet=data['rows']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0

    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        # acessa a primeira celula da linha (parceiro)
        celulaparceiro=linha['cells'][0]['value']
        
        # gera a linha formatada caso parceiro encontrado
        if parceiro in celulaparceiro.lower():
            msg=msg+("  \n**Partner:**"+celulaparceiro+"  \n")
            msg=msg+formata_SE(linha)
            encontrado=encontrado+1
        
        count=count+1

                    
    # devolva negativa caso nada encontrado
    if encontrado==0:
        msg=msg+"SE: Nenhum resultado encontrado.  "



    return msg

def smartsolution(parceiro):

    # Procura parceiros de solucao (por vertical, depois por nome de parceiro), retorna msg com dados ou resultado negativo caso nao encontrado
    # Daniel - 23.7.19

    if parceiro=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("solution")

    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg


    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    # loop para procurar por vertical

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        try:
            # acessa a segunda celula da linha (vertical)
            vertical=linha['cells'][1]['value']
            
            # gera a linha formatada caso parceiro encontrado
            
            if parceiro in vertical.lower():
                msg=msg+formata_solution(linha)
                encontrado=encontrado+1
        except:
            pass
        count=count+1

    # procura por parceiro Cisco caso nenhuma solucao vertical encontrada
    if encontrado==0:
        count=0
        while (count<linhas):

            # valida 1 linha por vez
            linha=data['rows'][count]

            try:
                # acessa a primeira celula da linha (parceiro)
                vertical=linha['cells'][0]['value']
                
                # gera a linha formatada caso parceiro encontrado
                
                if parceiro in vertical.lower():
                    msg=msg+formata_solution(linha)
                    encontrado=encontrado+1
            except:
                pass
            count=count+1

                                        
    
    
    # devolva negativa caso nada encontrado
    
    if encontrado==0:
        msg="Solution Partner: Nenhum resultado encontrado.  "


    return msg


def smartagenda(quarter):

    # Procura agenda de eventos
    # 26.7.2019
    if quarter=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("agenda")

    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg


    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        try:
            # acessa a primeira celula da linha (parceiro)
            linha_agenda=linha['cells'][0]['value']
            
            # gera a linha formatada caso parceiro encontrado
            
            if quarter in linha_agenda.lower():
                msg=msg+formata_agenda(linha)
                encontrado=encontrado+1
        except:
            pass
        count=count+1

                    
        # devolva negativa caso nada encontrado
    
    if encontrado==0:
        msg="Agenda: Nenhum resultado encontrado.  "


    return msg

def smartpid(pid):
    
    # Procura por pids
    # 13.9.2019
    if pid=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("pid")

    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg


    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        try:
            # acessa a primeira celula da linha (parceiro)
            linha_pid=linha['cells'][0]['value']
            
            # gera a linha formatada caso parceiro encontrado
            
            if pid in linha_pid.lower():
                msg=msg+formata_pid(linha)
                encontrado=encontrado+1
        except:
            pass
        count=count+1

                    
        # devolva negativa caso nada encontrado
    
    if encontrado==0:
        msg="Pid: Nenhum resultado encontrado.  "


    return msg



def smartdap(parceiro):

    # Procura infos DAP do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado
    # 19.7.2019
    if parceiro=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("dap")

    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg


    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        try:
            # acessa a primeira celula da linha (parceiro)
            celulaparceiro=linha['cells'][1]['value']
            
            # gera a linha formatada caso parceiro encontrado
            
            if parceiro in celulaparceiro.lower():
                msg=msg+formata_DAP(linha)
                encontrado=encontrado+1
        except:
            pass
        count=count+1

                    
        # devolva negativa caso nada encontrado
    
    if encontrado==0:
        msg="DAP: Nenhum resultado encontrado.  "


    return msg



def smartmeraki(parceiro):

    # Procura SE Certificado Meraki do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado
    # 19.7.2019

    if parceiro=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("meraki")


    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg


    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    #leva conteudo da planilha para variavel sheet
    #sheet=data['rows']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        try:
            # acessa a primeira celula da linha (parceiro)
            celulaparceiro=linha['cells'][0]['value']
            
            # gera a linha formatada caso parceiro encontrado
            
            if parceiro in celulaparceiro.lower():
                msg=msg+formata_SE_Meraki(linha)
                encontrado=encontrado+1
        except:
            pass
        count=count+1

                    
        # devolva negativa caso nada encontrado
    
    if encontrado==0:
        msg="SE: Nenhum resultado encontrado.  "


    return msg

def smartps(parceiro):

    # Procura SE de Public Sector do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("4PS")


    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg


    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        try:
            # acessa a primeira celula da linha (parceiro)
            celulaparceiro=linha['cells'][0]['value']
            
            # gera a linha formatada caso parceiro encontrado
            
            if parceiro in celulaparceiro.lower():
                msg=msg+formata_SE_PS(linha)
                encontrado=encontrado+1
        except:
            pass
        count=count+1

                    
        # devolva negativa caso nada encontrado
    
    if encontrado==0:
        msg="SE: Nenhum resultado encontrado.  "


    return msg



def smartmanager(parceiro):

    # Procura SEM do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("sem")


    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg


    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    #leva conteudo da planilha para variavel sheet
    #sheet=data['rows']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        # acessa a primeira celula da linha (parceiro)
        celulaparceiro=linha['cells'][0]['value']
        
        # gera a linha formatada caso parceiro encontrado
        if parceiro in celulaparceiro.lower():
            msg=msg+formata_SEM(linha)
            encontrado=encontrado+1
        
        count=count+1

                    
        # devolva negativa caso nada encontrado
    
    if encontrado==0:
        msg="SEM: Nenhum resultado encontrado.  "


    return msg

def smartpam(parceiro):

    # Procura PAM do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return

    # planilha do smartsheet
    # chama a funcao que busca planilha no smartsheet e devolve como JSON
    data = smartsheet("pam")


    # aborta caso nao tenha sido possivel acessar smartsheet
    if data=="erro":
        msg="Erro de acesso\n"
        return msg

    # quantas linhas tem a planilha
    linhas = data['totalRowCount']

    #leva conteudo da planilha para variavel sheet
    #sheet=data['rows']

    # loop para procurar o pam e imprime

    msg=""
    count=0
    encontrado=0
    
    while (count<linhas):

        # valida 1 linha por vez
        linha=data['rows'][count]

        # acessa a primeira celula da linha (parceiro)
        celulaparceiro=linha['cells'][0]['value']
        
        # gera a linha formatada caso parceiro encontrado
        if parceiro in celulaparceiro.lower():
            msg=msg+formata_PAM(linha)
            encontrado=encontrado+1
        
        count=count+1

                    
    # devolva negativa caso nada encontrado
    if encontrado==0:
        msg="PAM: Nenhum resultado encontrado.  "


    return msg


#########################################################
## FUNCOES de formatacao de texto para saida Webexteams

#########################################################


def formata_SEM(dados):

#monta linha do SEM

# zera variaveis
    
    msg=""
    semparceiro=""
    semcity=""
    semregion=""
    semtitle=""
    semname=""
    semmail=""
    semphone=""

    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        semparceiro=dados['cells'][0]['value']
    except:
        pass
    try:
        semcity=dados['cells'][1]['value']
    except:
        pass
    try:
        semregion=dados['cells'][2]['value']
    except:
        pass
    try:
        semtitle=dados['cells'][3]['value']
    except:
        pass
    try:
        semname=dados['cells'][4]['value']
    except:
        pass
    try:
        semmail=dados['cells'][5]['value']
    except:
        pass
    try:
        semphone=dados['cells'][6]['value']
    except:
        pass

    #monta a linha e imprime
    
    msg=msg+("**Manager:**"+semname+" **Partner:**"+semparceiro+" **Title:**"+semtitle+" "+semphone+" "+semmail+"  \n")
    msg=msg+("**Region:**"+semregion+" "+semcity+"  \n\n")


    return msg


def formata_SE_Meraki(dados):

#monta linha do SE

# zera variaveis
    
    msg=""
    separceiro=""
    senome=""
    sesobrenome=""
    semail=""
    
    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        separceiro=dados['cells'][0]['value']
    except:
        pass
    try:
        senome=dados['cells'][1]['value']
    except:
        pass
    try:
        sesobrenome=dados['cells'][2]['value']
    except:
        pass
    try:
        semail=dados['cells'][12]['value']
    except:
        pass
 
    #monta a linha e imprime
    
    msg=msg+("**Certified SE:**"+senome+" "+sesobrenome+"** Partner:**"+separceiro+" "+semail+"  \n\n")
   
    return msg

def formata_SE_PS(dados):

#monta linha do SE PS

# zera variaveis
    
    msg=""
    separceiro=""
    senome=""
    selocalidade=""
    semail=""
    secompet=""
    
    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        separceiro=dados['cells'][0]['value']
    except:
        pass
    try:
        senome=dados['cells'][1]['value']
    except:
        pass
    try:
        semail=dados['cells'][2]['value']
    except:
        pass
    try:
        selocalidade=dados['cells'][3]['value']
    except:
        pass
    try:
        secompet=dados['cells'][4]['value']
    except:
        pass
 
    #monta a linha e imprime
    
    msg=msg+("**Parceiro:**"+separceiro+" **Nome:**"+senome+" "+semail+" "+selocalidade+"  \n")
    msg=msg+("**Arquiteturas que cobre:"+secompet+"  \n\n")
   
    return msg

def formata_solution(dados):

#monta linha de parceiros de solucao

# zera variaveis
    
    msg=""
    vparceiro=""
    vertical=""
    vsolution=""
    vdescription=""
    
    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        vparceiro=dados['cells'][0]['value']
    except:
        pass
    try:
        vertical=dados['cells'][1]['value']
    except:
        pass
    try:
        vsolution=dados['cells'][2]['value']
    except:
        pass
    try:
        vdescription=dados['cells'][3]['value']
    except:
        pass
    
    #monta a linha e imprime
    
    msg=msg+("**Parceiro:**"+vparceiro+" **Vertical:**"+vertical+"  \n")
    msg=msg+("**Nome da oferta:** "+vsolution+"  \n")
    msg=msg+("**Descrição da oferta:**"+vdescription+"  \n\n")
   
    return msg


def formata_SE(dados):

# monta linha do SE

# zera variaveis
    
    msg=""
    separceiro=""
    sename=""
    setel=""
    semail=""
    secomp=""
    

    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        separceiro=dados['cells'][0]['value']
    except:
        pass
    try:
        sename=dados['cells'][1]['value']
    except:
        pass
    try:
        setel=dados['cells'][2]['value']
    except:
        pass
    try:
        semail=dados['cells'][3]['value']
    except:
        pass
    try:
        secomp=dados['cells'][4]['value']
    except:
        pass
    
    #identifica competencias
    compet=""
    for x in secomp.split(','):
        
        # remove espacos em branco nas laterais
        x=x.rstrip()
        x=x.lstrip()
            
        if x !="":
            compet = compet + " " + x + " "

    #monta a linha e imprime
   
    msg=msg+("**SE:** "+sename+": "+semail+" "+setel+"  \n")
    # imprime competencias somente se tiver
    if compet != "":
        msg=msg+("**Competencies:**"+compet+"  \n")
            
    return msg


def formata_PAM(dados):

#monta linha do PAM

# zera variaveis
    
    msg=""
    pamparceiro=""
    pamname=""
    pamcity=""
    pammail=""
    pamphone=""
  
    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        pamparceiro=dados['cells'][0]['value']
    except:
        pass
    try:
        pamcity=dados['cells'][1]['value']
    except:
        pass
    try:
        pamname=dados['cells'][2]['value']
    except:
        pass
    try:
        pammail=dados['cells'][3]['value']
    except:
        pass
    try:
        pamphone=dados['cells'][4]['value']
    except:
        pass
    
    #monta a linha e imprime
    
    msg=msg+("**PAM do Parceiro:** "+pamparceiro+": "+pamname+" "+pammail+"@cisco.com "+pamphone+" "+pamcity+"  \n\n")
 

    return msg


def formata_agenda(dados):

#agenda de eventos para parceiros
#26-07-19

# zera variaveis
    
    msg=""
    quarter=""
    mes=""
    evento=""
    dia_programado=""
    localidade=""
  
    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        quarter=dados['cells'][0]['value']
    except:
        pass
    try:
        mes=dados['cells'][1]['value']
    except:
        pass
    try:
        evento=dados['cells'][2]['value']
    except:
        pass
    try:
        dia_programado=dados['cells'][3]['value']
    except:
        pass
    try:
        localidade=dados['cells'][4]['value']
    except:
        pass
    
    #monta a linha e imprime
    
    msg=msg+("**Evento**: "+evento+" **Local:** "+localidade+" "+dia_programado+"  \n\n")
 

    return msg

def formata_pid(dados):

    #lista de pids
    #13.09.2019
    
    # zera variaveis
        
        msg=""
        pid=""
        qty_available=""
        updated=""
        updated_by=""
        localidade=""
      
        # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
        try:
            pid=dados['cells'][0]['value']
        except:
            pass
        try:
            qty_available=dados['cells'][7]['value']
        except:
            pass
        try:
            updated_by=dados['cells'][8]['value']
        except:
            pass
        try:
            updated=dados['cells'][9]['value']
        except:
            pass
        
        #monta a linha e imprime
        
        msg=msg+("**PID**: "+pid+" **Quantidade:** "+qty_available+" **Atualizado:** "+updated+" "+updated_by+"  \n\n")
     
    
        return msg
    

def formata_DAP(dados):

#monta linha do PAM

# zera variaveis
    
    msg=""
    dapparceiro=""
    dapcert=""
    dapdist=""
    dappam=""
    dapskills=list()
    dapcontacts=list()
  
    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        dapparceiro=dados['cells'][1]['value']
    except:
        pass
    try:
        dapcert=dados['cells'][3]['value']
    except:
        pass
    try:
        dapdist=dados['cells'][4]['value']
    except:
        pass
    try:
        dappam=dados['cells'][7]['value']
    except:
        pass
    
    # monta lista de competencias do parceiro, caso tenha
    try:
        dapskills.append(dados['cells'][8]['value'])
    except:
        pass
    try:
        dapskills.append(dados['cells'][9]['value'])
    except:
        pass
    try:
        dapskills.append(dados['cells'][10]['value'])
    except:
        pass
    try:
        dapskills.append(dados['cells'][11]['value'])
    except:
        pass
    try:
        dapskills.append(dados['cells'][12]['value'])
    except:
        pass
    try:
        dapskills.append(dados['cells'][13]['value'])
    except:
        pass
    # monta lista de contatos do dist, caso tenha    
    try:
        dapcontacts.append(dados['cells'][14]['value'])
    except:
        pass
    try:
        dapcontacts.append(dados['cells'][15]['value'])
    except:
        pass
    try:
        dapcontacts.append(dados['cells'][16]['value'])
    except:
        pass
    
    

    #monta a linha e imprime
    
    # competencias
    compet=""
    for b in dapskills:
        if b!="":
            compet=compet+b+' '

    # contatos Dist
    contacts=""
    for b in dapcontacts:
        if b!="":
            contacts=contacts+b+' '

    msg=msg+("\n**Parceiro:** "+dapparceiro+": **Certificacao:**"+dapcert+"  \n")
    msg=msg+("**PAM:** "+dappam+"** DAP do Distribuidor:**"+dapdist+"  \n")
    msg=msg+("**Especializacoes:**"+compet+"  \n")
    msg=msg+("**Contato no Dist:**"+contacts+"  \n")

    return msg




#########################################################
## FUNCOES API Suporte Cisco

#########################################################

def ajuda():

    # Funcao ajuda deste bot
    msg="""
Forma de uso:  \n
**Procurar Systems Engineer (SE) dos parceiros:**  \n
___
Procurar SE do parceiro: se ***dna|dc|sec|collab*** partner ***nome do parceiro***  \n
Procurar SE de Public Sector: seps partner ***nome do parceiro***  \n
Procurar Certificado Meraki: meraki partner ***nome do parceiro***  \n
Procurar Manager do Parceiro: manager partner ***nome do parceiro**  \n\n
**Procurar Ajuda sobre os Parceiros:**  \n
___
Procurar PAM do parceiro: pam partner ***nome do parceiro***  \n
Procura Parceiro por solução: solution partner ***nome da vertical*** ou ***nome do parceiro***  \n
Procurar Distribuidor do parceiro: dap partner ***nome do parceiro***  \n\n
Detalhe do Parceiro: detail partner ***nome do parceiro***  \n\n
**Procurar Ajuda para Parceiros:**  \n

Agenda para parceiros: agenda partner ***quarter***  \n
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
