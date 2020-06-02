from funcoes_Cisco import ajuda, smartpid,ft, autorizauser
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
    #print("comando:")
    #print(comando)

    # identifica e trata comandos relacionados a parceiros - palavra chave partner
    # logo a primeira parte do comando e' o que queremos procurar e
    # a segunda e' o nome do parceiro
    # logo comando = o comando completo, box = funcao esperada e parceiro = nome do parceiro
    #sp=comando.split("partner")
    #sp=comando.split("disti")
    lista_comando=comando.split()
    #print ("lista de comandos:")
    #print(lista_comando)
    qty_comandos = len(lista_comando)
    #print("qt de comandos:")
    #print(qty_comandos)

    # comando ou a primeira palavra na variavel box
    box=lista_comando[0]
    # ajusta a segunda variavel com o nome do parceiro eliminando elista_comandoacos a esquerda e direita
    #if len(lista_comando)>1:
    #    disti=lista_comando[1].strip()
    #    print ("dist:")
    #    print(disti)
        # remove elista_comandoacos no final, caso existam
        #parceiro=parceiro.rstrip()


    #msg=""

    # Comandos para todos usuários:

    if "help" in comando:
        msg=ajuda()

    # Funcoes somente para users Cisco

    else:
        #verifica se o usuários é da Cisco
        if autorizauser(usermail)==True:

            if lista_comando[0] == "estoque":
                # funcoes relacionadas a parceiro
                #comandos para usuarios Cisco:
                #Comando tipo "pid pid_id"
                if len (lista_comando) == 1:
                    msg = "Digite o partnumber desejado. Utilizar 'help' para saber os comandos válidos disponíveis."
                    return msg
                if len(lista_comando) == 2:
                    pid = lista_comando[1]
                    print(str(pid.lower()))
                    if pid.lower() =="" or None:
                        msg = "Digite o partnumber desejado. Utilizar 'help' para saber os comandos válidos disponíveis."
                        return msg
                    #elif str(pid.lower()) == "fabrica" or "comstor" or "ingram" or "scansource" or "alcateia":
                    #    msg = "Partnumber do produto não é válido. Utilizar 'help' para saber os comandos válidos disponíveis."
                    #    return msg
                    #print("pid:")
                    #print (pid)
                    local = "All"
                    #print ("Local:")
                    #print (local)
                    msg=smartpid(pid,local)
                    #return smartpid(pid,local) len
                    return msg
            
                #Comando tipo "pid local_id pid_id"
                elif len(lista_comando) == 3:
                    pid = lista_comando[2]
                    #print("pid:")
                    #print (pid)
                    local = lista_comando[1]
                    lista_de_locais = ["comstor","ingram","scansource"]
                    if pid.lower() in lista_de_locais:
                        msg = "Partnumber do produto não é válido. Utilizar 'help' para saber os comandos válidos disponíveis."
                        return msg
                    #print ("Local:")
                    #print (local)
                    msg=smartpid(pid,local)
                    #return smartpid(pid,local)
                    return msg
                else:
                    msg = "Desculpe não conheço esse comando, utilizar 'help' para saber os comandos disponíveis."
                    return msg
                    
            
                #Nenhum comando conhecido

            if lista_comando[0] == "ft":
                 
                if len (lista_comando) == 1:
                    msg = "Digite 'ft + local' para verificar quais equipamentos participam do programa FastTrack."
                    return msg
                if len(lista_comando) == 2:
                    local = lista_comando[1]
                    print(str(local.lower()))
                                         
                    msg=ft(local)
                    
                

        else:
            msg = "Você não está autorizado a utilizar esses comandos"
            return msg





    if msg=="" or msg==None:
       #return
       msg="Use 'help' for help :-)"
       return msg

    return msg
