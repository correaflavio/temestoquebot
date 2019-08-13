from funcoes_Cisco import ajuda, smartpid, autorizauser
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
    print("comando:")
    print(comando)
    
    # identifica e trata comandos relacionados a parceiros - palavra chave partner
    # logo a primeira parte do comando e' o que queremos procurar e
    # a segunda e' o nome do parceiro
    # logo comando = o comando completo, box = funcao esperada e parceiro = nome do parceiro
    #sp=comando.split("partner")
    #sp=comando.split("disti")
    lista_comando=comando.split()
    print ("lista de comandos:")
    print(lista_comando)
    qty_comandos = len(lista_comando)
    print("qt de comandos:")
    print(qty_comandos)

    # comando ou a primeira palavra na variavel box
    #box=lista_comando[0]
    #print ("box:") 
    #print(box)

    # ajusta a segunda variavel com o nome do parceiro eliminando elista_comandoacos a esquerda e direita
    #if len(lista_comando)>1:
    #    disti=lista_comando[1].strip()
    #    print ("dist:")
    #    print(disti)
        # remove elista_comandoacos no final, caso existam
        #parceiro=parceiro.rstrip()

    
    msg=""
    
    # chamadas de acordo com os parametros

    # Funcoes somente para users Cisco

    if autorizauser(usermail)==True:
        # funcoes relacionadas a parceiro
        #if "partner" in comando:
        if len(lista_comando) == 2:
            pid = lista_comando[1]
            print("pid:")
            print (pid)
            local = "All"
            print ("Local:")
            print (local)
            msg=smartpid(pid,local)
        
        elif len(lista_comando) == 3:
            pid = lista_comando[2]
            print("pid:")
            print (pid)
            local = lista_comando[1]
            print ("Local:")
            print (local)
            msg=smartpid(pid,local)


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
