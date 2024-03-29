import sys
import re
import os
import time

#variáveis para mudar cores no terminal
RED   = "\033[1;31m"
RESET = "\033[0;0m"

#classe para representar cada transição de cada estado
class Transicao:
    def __init__(self,estadoDestino,troca,movimento,estadoAtual,leitura):
        self.estadoDestino = estadoDestino
        self.troca = troca
        self.movimento = movimento
        self.estadoAtual = estadoAtual
        self.leitura = leitura

#função para decodificar os símbolos da fita de entrada
def simbolo(valor):
    dic = {1: 'a', 2:'b',3:'B'}
    return(dic[valor])

#função para decodificar os movimentos da cabeça de leitura
def direcao(valor):
    dic = {1: 'R', 2:'L'}
    return(dic[valor])

#separa a representação da máquina da palavra e retorna duas listas
def decodificaEntrada(entrada):
    maquina = []
    palavra = []
    flagFimMaquina = False
    countZero = 0
    for i in range(len(entrada)):
        if(not flagFimMaquina):
            if(entrada[i] != "\n"):
                maquina.append(entrada[i])
                if(entrada[i] == '0'):  
                    countZero = countZero + 1
                else:
                    countZero = 3
                if(countZero == 6):
                    flagFimMaquina = True
        else:
            if(entrada[i] != "\n"):
                palavra.append(entrada[i])
        
    return maquina,palavra

#função utilizada para ler o arquivo
def lerArquivo():
    arquivo = sys.argv[1]
    f = open(arquivo,'r')
    data = f.read()
    f.close()
    return data

#função utilizada para verificar se a máquina e a palavra de entrada são válidas utilizando expressão regular
def verificaMTU(texto):
    expressao="(000)(((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+)00))*((1+)(0)(1+)(0)(1+)(0)(1+)(0)(1+))(000)(1+)(01+)*(000)"
    x = bool(re.match(expressao,str(texto)))
    if(x):
        return True
    else:
        print("False")
        return False

#decodifica a palavra de entrada com representação unária para Strings
def decodificaFita(palavra):
    fitaEntrada = []
    count = 0
    for i in range(len(palavra)):
        if(palavra[i] == "0"):
            count = 0
        else:
            count = count + 1
            if(i<(len(palavra)-1)):
                if(palavra[i+1] == "0"):
                    fitaEntrada.append(simbolo(count))
                    count = 0
    
    fitaEntrada.append("B")
    
    return fitaEntrada

#função utilizada para achar a próxima transição na representação unária
def moveRight(posicao, maquina):
    while(maquina[posicao]!="1" and posicao < len(maquina)-1):
        posicao = posicao + 1
    return posicao

def maiorEstadocomTransicao(maquina):
    posicao = len(maquina)-4
    #print(maquina[posicao])
    ultimaPosicao = -1
    countZero = 0
    while(countZero <2):
        if(maquina[posicao] == "0"):
            countZero = countZero+1
            posicao = posicao -1
        else:
            countZero = 0
            posicao = posicao -1
    posicao = posicao+1
    while(maquina[posicao]!="1"):
        posicao = posicao+1

    while(maquina[posicao]== "1"):
        ultimaPosicao = ultimaPosicao+1
        posicao = posicao+1

    return ultimaPosicao
#função utilizada para transformar cada transição em representação unária em um objeto do tipo Transição
def decodificaMaquina(maquina):
    transicoes = []
    estado = []
    posicao = 3
    acabou = False
    estadoAtualAux = 0
    while(posicao < len(maquina)-1):
        estadoDestino = -1
        troca = 0
        movimento = 0
        estadoAtual = -1
        leitura = 0
        while(maquina[posicao] != "0"):
            estadoAtual = estadoAtual +1
            posicao = posicao +1
        posicao = posicao +1
        while(maquina[posicao] != "0"):
            leitura = leitura + 1
            posicao = posicao +1
        posicao = posicao +1
        while(maquina[posicao] != "0"):
            estadoDestino = estadoDestino + 1
            posicao = posicao +1
        posicao = posicao +1
        while(maquina[posicao] != "0"):
            troca = troca + 1
            posicao = posicao +1
        posicao = posicao +1
        while(maquina[posicao] != "0" and posicao < len(maquina)-1):
            movimento = movimento + 1
            posicao = posicao +1
        
        oEstado = Transicao(estadoDestino,troca,movimento,estadoAtual,leitura)        
        if((estadoAtualAux == estadoAtual)):
            estado.append(oEstado)
        else:
            transicoes.append(estado)
            estado = []
            estado.append(oEstado)
            estadoAtualAux = oEstado.estadoAtual
        posicao = moveRight(posicao,maquina)
    
    if(oEstado.estadoAtual == maiorEstadocomTransicao(maquina)):
        if(oEstado not in estado):
            estado.append(oEstado)
        transicoes.append(estado)
    
    return transicoes

#execução da máquina
def executar(transicoes,fita):
    os.system("clear")
    estadoAtual = 0
    terminou = False
    posicaoFita = 0
    loopH1= False
    loopH2= False 
    while(not terminou):
        achouTransicao = False
        for i in range(len(transicoes[estadoAtual])):
            if(len(transicoes[estadoAtual]) == 3):
                if(transicoes[estadoAtual][0].estadoAtual == transicoes[estadoAtual][0].estadoDestino and transicoes[estadoAtual][1].estadoAtual == transicoes[estadoAtual][1].estadoDestino and transicoes[estadoAtual][2].estadoAtual == transicoes[estadoAtual][0].estadoDestino):
                    if(len(fita)-1 != int(posicaoFita) and len(fita)-1 != int(posicaoFita)-1):
                        loopH2=True
                        break
                if(transicoes[transicoes[estadoAtual][0].estadoDestino][0].estadoAtual==transicoes[transicoes[estadoAtual][0].estadoDestino][0].estadoDestino and transicoes[transicoes[estadoAtual][1].estadoDestino][1].estadoAtual==transicoes[transicoes[estadoAtual][1].estadoDestino][1].estadoDestino and transicoes[transicoes[estadoAtual][2].estadoDestino][2].estadoAtual==transicoes[transicoes[estadoAtual][2].estadoDestino][2].estadoDestino):
                    loopH1=False
                    loopH2=False
                    break
            if(not loopH2):
                if(simbolo(transicoes[estadoAtual][i].leitura) != fita[posicaoFita]):
                    if(len(fita)-1 != int(posicaoFita)):
                        loopH1= True

                else:
                    loopH1=False
                    print("Estado Atual:", estadoAtual)
                    print("Conteudo da Fita:", fita[posicaoFita])
                    print("Direcao Cabeça de Leitura:",direcao(transicoes[estadoAtual][i].movimento))
                    print("Troca por: ", simbolo(transicoes[estadoAtual][i].troca))
                    fita[posicaoFita] = simbolo(transicoes[estadoAtual][i].troca)
                    posicaoFitaAux = posicaoFita
                    if(direcao(transicoes[estadoAtual][i].movimento) == "R"):
                        posicaoFita = posicaoFita+1
                    elif(direcao(transicoes[estadoAtual][i].movimento) == "L"):
                        posicaoFita = posicaoFita-1
                    estadoAtual = transicoes[estadoAtual][i].estadoDestino

                    for j in range(len(fita)):
                        if(j==posicaoFitaAux):
                            print(RED,end="")
                            print(fita[j],end="")
                        else:
                            print(RESET,end="")
                            print(fita[j],end="")                        
                    print(RESET)
                    if(estadoAtual >= len(transicoes)):
                        achouTransicao = False
                        break

                    achouTransicao = True
                    time.sleep(0.7)
                    os.system("clear")
    
        if(not achouTransicao):
            terminou = True

    time.sleep(0.7)
    os.system("clear")
    if(posicaoFita>=len(fita)-1):
        posicaoFita = len(fita)-1
    print("Estado Atual:", estadoAtual)
    print("Conteudo da Fita:", fita[posicaoFita])
    print("Direcao Cabeça de Leitura: NULL")
    for j in range(len(fita)):
        if(j==posicaoFita):
                    print(RED,end="")
                    print(fita[j],end="")
        else:
                    print(RESET,end="")
    
                    print(fita[j],end="")
    
    print()
    if(loopH1 or loopH2):
        if(loopH1):
            print("Esta maquina entraria em loop(através da Heuristica Decididora) para esta entrada.")
        if(loopH2):
            print("Esta maquina entraria em loop(através da Heuristica Reconhecedora) para esta entrada.")
    else:
        print("Esta maquina NAO entraria em loop para esta entrada.")
    
                
def main():
    arquivo = lerArquivo()
    if(verificaMTU(arquivo) == True ):
        maquina,palavra = decodificaEntrada(arquivo)
        fita = decodificaFita(palavra)
        maiorEstadocomTransicao(maquina)
        transicoes = decodificaMaquina(maquina)
        '''
        for i in range(len(transicoes)):
            for j in range(len(transicoes[i])):
                print("Estado Atual: ",transicoes[i][j].estadoAtual," Lendo: ",simbolo(transicoes[i][j].leitura)," Vai para: ",transicoes[i][j].estadoDestino)
        '''
        executar(transicoes,fita)
        
    else:
        print("Entrada inválida")
main()