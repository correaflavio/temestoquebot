from funcoes_Cisco import ajuda, smartmanager, smartmeraki, smartpam, smartse, autorizauser, smartps, smartdap, smartsolution, smartagenda
from prime import testa_prime,prime_produto,prime_servico
from webexteams import getwebexRoomID, webexmsgRoomviaID

def logica(comando,usermail):

    # faz a logica de entender o comando pedido e a devida resposta para o usuario
    # o parametro usermail e' utilizado para identificar o usuario que solicitou o comando
    # O usuario pode ser uzado como filtro para se executar ou negar o comando
    #
    # Retorna mensagem para ser enviada para console ou Webex teams
    
    #Separa o comando por espacos
    #Primeiro item e'o comando em si, os demais sao parametros deste comando
    #tudo minusculo
    comando=comando.lower()
    
    # identifica e trata comandos relacionados a parceiros - palavra chave partner
    # logo a primeira parte do comando e' o que queremos procurar e
    # a segunda e' o nome do parceiro
    # logo comando = o comando completo, box = funcao esperada e parceiro = nome do parceiro
    sp=comando.split("partner")
    # comando ou a primeira palavra na variavel box
    box=sp[0]

    # ajusta a segunda variavel com o nome do parceiro eliminando espacos a esquerda e direita
    if len(sp)>1:
        parceiro=sp[1].strip()
        # remove espacos no final, caso existam
        #parceiro=parceiro.rstrip()

    
    msg=""
	
    # chamadas de acordo com os parametros

    # Funcoes somente para users Cisco

    if autorizauser(usermail)==True:
        # funcoes relacionadas a parceiro
        if "partner" in comando:
    
            if "manager" in box:
                msg=smartmanager(parceiro)

            # pam do parceiro
            if "pam" in box:
                msg=smartpam(parceiro)
    
            if "se" in box:
                if "sec" in box:
                    msg=smartse(parceiro,"sec",box)
                elif "dc" in box:
                    msg=smartse(parceiro,"dc",box)
                elif "dna" in box:
                    msg=smartse(parceiro,"dna",box)
                elif "col" in box:
                    msg=smartse(parceiro,"collab",box)
                else:
                    msg="use: se ***dc|dna|sec|collab*** partner ***partner name***"

            # procura SE certificado Meraki
            if "meraki" in box:
                msg=smartmeraki(parceiro)

            # procura SE de PS
            if "seps" in box:
                msg=smartps(parceiro)
            
            # procura dados DAP do parceiro
            if "dap" in box:
                msg=smartdap(parceiro)

            # procura parceiro por solucao - J. Sardinha - 23.7.19
            if "solution" in box:
                msg=smartsolution(parceiro)

            # procura agenda para parceiros - 26.7.19
            if "agenda" in box:
                # a variavel parceiro aqui na verdade leva o quarter procurado exemplo: q1
                msg=smartagenda(parceiro)
                
            # procura pids no estoque - 13.9.19
            if "pid" in box:
                # a variavel parceiro aqui na verdade leva o pid procurado exemplo: 2960X
                msg=smartpid(parceiro)

            if "detail" in box and parceiro != "":
                msg=smartpam(parceiro)
                msg=msg+smartmanager(parceiro)

        
        # função prime - 16-7-2019

        if "desconto prime" in comando:

            correto="**Uso Correto:** desconto prime ***produto*** ou ***servico*** ***valor_prime*** ***valor_diferenca***.  \n**Exemplo:** desconto prime servico 65 30  \n"
            
            # Transforma comando em parametros
            parametros=comando.split()
            # testa se tem o minimo de parametros
            if len(parametros)==5:
                tipo=parametros[2]
                prime=int(parametros[3])
                diferenca=int(parametros[4])

                # primeiro testa se intervalo de prime e diferenca sao razoaveis
                if testa_prime(prime,diferenca)=="ok":
                    if "prod" in tipo:
                        # executa calculo prime para produto
                        msg=prime_produto(prime,diferenca)
                    elif "serv" in tipo or "svc" in tipo:
                        # executa calculo prime para servico
                        msg=prime_servico(prime,diferenca)
                    else:
                        # do contrario mensagem de erro com a sintaxe correta
                        msg=correto
                else:
                    # erro pois intervalos de prime e diferenca incorretos
                    msg="Intervalos de prime e/ou diferenca incorretos."
            else:
                # mensagem de erro pois nao tem o minimo de parametros
                msg=correto

    if "help" in comando:
        msg=ajuda()

    # Funcoes para todos

    
    if msg=="" or msg==None:
        msg="Use 'help' for help :-)"

    # 26-7-19
    # tenta logar tudo na sala "log do partnerbot"
    try:
        log="user:"+usermail+" comando:"+comando
        webexmsgRoomviaID(getwebexRoomID("Log do TemEstoque"),log)
    except:
        pass

    return msg
