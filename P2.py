'''
    desvio incondicional = 0000
    desvio se 0 = 0001
    desvio se negativo = 0010
    soma = 0011
    subtracao = 0100
    multiplicacao = 0101
    divisao = 0110
    Load = 0111
    store = 1000
    call = 1001
    end = 1010
    data = 1011
    return = 1100
    stop = 1101
'''

import sys

'''
Função que implementa o Loader;
Tem como entrada a fita com o programa objeto
Tem como saída a memória simulada com o programa executável nela e o endereço inicial das instruções.
'''
def Loader(fita):
    endereco = ''
    memoria = simula_memoria()
    i = 1
    while i < 4:
        endereco += fita[i]
        i += 1
    i = 4
    endereco = hexadecimal_decimal(endereco)
    endereco_inicial = endereco
    
    while True:
        
        comando = converte_hexadecimal(fita[i])
        if comando == '1100' or comando == '1101':
            memoria[endereco] = comando
            memoria[endereco + 1] = converte_hexadecimal(fita[i+1])
            i += 2
            endereco += 2
        elif comando == '1010':
            memoria[endereco] = comando
            memoria[endereco + 1] = converte_hexadecimal(fita[i+1])
            break
        elif comando == '1011':
            memoria[endereco] = converte_hexadecimal(fita[i+1])
            memoria[endereco + 1] = converte_hexadecimal(fita[i+2])
            memoria[endereco + 2] = converte_hexadecimal(fita[i+3])
            i += 4
            endereco += 3
        else:
            memoria[endereco] = comando
            memoria[endereco + 1] = converte_hexadecimal(fita[i+1])
            memoria[endereco + 2] = converte_hexadecimal(fita[i+2])
            memoria[endereco + 3] = converte_hexadecimal(fita[i+3])
            i += 4
            endereco += 4
    return memoria, endereco_inicial

'''
Função que implemente a máquina de instruções, que é o motor de eventos principal do projeto;
Tem como entrada a memória simualada, o endereço inicial das instruções, o registrador e as flags;
Não possui saída 
'''


def maquina_instrucoes(memoria, endereco, reg, flags):
    '''máquina de instruções'''
    while True:
        comando = memoria[endereco]
        if comando != '1100' and comando != '1101':
            
            dados = memoria[endereco + 1] + memoria[endereco + 2] + memoria[endereco + 3]
            print('Próxima Instrução:')
            imprime_instrucao(binario_hexa(comando), binario_hexa(dados))
            proxima_instrucao(memoria)
            if comando == '0000' or comando == '0001' or comando == '0010':#Desvios
                endereco += 4
                endereco = funcao_desvio(comando, dados, endereco, flags)
            elif comando == '0011' or comando == '0100' or comando == '0101' or comando == '0110': #Operações aritméticas
                reg = funcao_aritmetica(comando, dados, reg, flags)
                endereco += 4
            elif comando == '0111': #Operações aritméticas
                reg = funcao_load(dados, flags, memoria)
                endereco += 4
            elif comando == '1000':
                funcao_store(dados, reg, memoria)
                endereco += 4
            elif comando == '1001':
                print('\nInstrução Realizada:')
                imprime_instrucao(binario_hexa(comando), binario_hexa(dados))
                print('Valor do registrador (binário):', reg)
                print('Valor do registrador (hexadecimal):', binario_hexa(reg))
                print('Valor do registrador (decimal):', binario_decimal(reg, 12, True))
                print('flags:', flags)
                maquina_instrucoes(memoria, binario_decimal(dados, 12, False), reg, flags)
                endereco += 4
            else:
                sys.exit()

        else:
            dados = '0'
            print('Próxima Instrução:')
            imprime_instrucao(binario_hexa(comando), binario_hexa(dados))
            proxima_instrucao(memoria)
            if comando == '1100':
                print('\nInstrução Realizada:')
                imprime_instrucao(binario_hexa(comando), binario_hexa(dados))
                print('Valor do registrador (binário):', reg)
                print('Valor do registrador (hexadecimal):', binario_hexa(reg))
                print('Valor do registrador (decimal):', binario_decimal(reg, 12, True))
                print('flags:', flags)
                return
            elif comando == '1101':
                funcao_stop()
                endereco += 2
        if comando != '1001':
            print('\nInstrução Realizada:')
            imprime_instrucao(binario_hexa(comando), binario_hexa(dados))
            print('Valor do registrador (binário):', reg)
            print('Valor do registrador (hexadecimal):', binario_hexa(reg))
            print('Valor do registrador (decimal):', binario_decimal(reg, 12, True))
            print('flags:', flags)


'''
Função que interrompe o motor de eventos até segunda ordem.
'''


def funcao_stop():
    while True:
        continua = input('************************\nMáquina de instruções em pausa, caso deseje continuar de onde parou digite c\n************************\n')
        if continua == 'c':
            return
        
'''
Função usada para salvar o valor do registrador na memória
'''
            
def funcao_store(dados_bin, reg, memoria):
    dados = binario_decimal(dados_bin, 12, False)
    memoria[dados] = reg[0] + reg[1] + reg[2] + reg[3]
    memoria[dados + 1] = reg[4] + reg[5] + reg[6] + reg[7]
    memoria[dados + 2] = reg[8] + reg[9] + reg[10] + reg[11]

'''
Função usada para buscar um valor na memória, que será salvo no registrador
'''

def funcao_load(dados_bin, flags, memoria):
    dados = binario_decimal(dados_bin, 12, False)
    valor = memoria[dados]+memoria[dados + 1] + memoria[dados + 2]
    if binario_decimal(valor, 12, True) < 0:
        flags[0] = 1
        flags[1] = 0
    elif binario_decimal(valor, 12, True) == 0:
        flags[0] = 0
        flags[1] = 1
    else:
        flags[0] = 0
        flags[1] = 0
    return valor

'''
Função usada para realizar as operações aritméticas (+, -, *, //)
'''
    
def funcao_aritmetica(comando, dados, reg, flags):
    reg_dec = binario_decimal(reg, 12, True)
    dados_dec = binario_decimal(dados, 12, True)
    if comando == '0011':
        retorno = dados_dec + reg_dec
    if comando == '0100':
        retorno = reg_dec - dados_dec
    if comando == '0101':
        retorno = dados_dec*reg_dec
    if comando == '0110':
        retorno = reg_dec // dados_dec
    if retorno == 0:
        flags[0] = 0
        flags[1] = 1
    elif retorno < 0:
        flags[0] = 1
        flags[1] = 0
    else:
        flags[0] = 0
        flags[1] = 0
    retorno_binario = decimal_binario(retorno, 12)
    return(retorno_binario)

'''
Função usada para as operações de desvio incondicional, desvio se negativo e desvio se zero
'''
    

def funcao_desvio(comando, dados, endereco,  flags):

    if comando == '0000':
        return binario_decimal(dados, 12, False)
    if comando == '0001':
        if flags[1] == 1:
            return binario_decimal(dados, 12, False)
        else:
            return endereco
    if comando == '0010':
        if flags[0] == 1:
            return binario_decimal(dados, 12, False)
        else:
            return endereco

'''
Funções auxiliares 
'''

'''
Função que simula memória
'''             
def simula_memoria():
    return ['0000']*4096


'''
Função que imprime código em linguagem de montagem a partir de uma fita
'''   
    
def imprimir_assembly(fita):
    i = 0
    var = fita[1] + fita[2] + fita[3]
    print('1 -          ORG     ', var)
    linha = 2
    i += 4
    while i < len(fita):
        if fita[i] == '0':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          JUMP    ', var)
            i += 4
            linha += 1
        elif fita[i] == '1':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          JUMP0  ', var)
            i += 4
            linha += 1
        elif fita[i] == '2':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          JUMPN   ', var)
            i += 4
            linha += 1
        elif fita[i] == '3':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          ADD     ', var)
            i += 4
            linha += 1
        elif fita[i] == '4':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          SUB     ', var)
            i += 4
            linha += 1
        elif fita[i] == '5':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          MUL     ', var)
            i += 4
            linha += 1
        elif fita[i] == '6':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          DIV     ', var)
            i += 4
            linha += 1
        elif fita[i] == '7':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          LOAD    ', var)
            i += 4
            linha += 1
        elif fita[i] == '8':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          STORE   ', var)
            i += 4
            linha += 1
        elif fita[i] == '9':
            var = fita[i + 1] + fita[i + 2] + fita[i +3]
            print(linha,'-          CALL    ', var)
            i += 4
            linha += 1
        elif fita[i] == 'A':
            print(linha,'-          END')
            break
        elif fita[i] == 'C':
            var = fita[i + 1]
            print(linha,'-          RTN     ', var)
            i += 2
            linha += 1
        elif fita[i] == 'D':
            print(linha,'-          STOP')
            i += 2
            linha += 1
        else:
            i += 4


'''
Função que imprime uma única instrução
'''   

    
def imprime_instrucao(instrucao, var):

        if instrucao == '0':
            print('JUMP    ', var)
        elif instrucao == '1':
            print('JUMP0  ', var)
        elif instrucao == '2':
            print('JUMPN   ', var)
        elif instrucao == '3':
            print('ADD     ', var)
        elif instrucao == '4':
            print('SUB     ', var)
        elif instrucao == '5':
            print('MUL     ', var)
        elif instrucao == '6':
            print('DIV     ', var)
        elif instrucao == '7':
            print('LOAD    ', var)
        elif instrucao == '8':
            print('STORE   ', var)
        elif instrucao == '9':
            print('CALL    ', var)
        elif instrucao == 'A':
            print('END')
        elif instrucao == 'C':
            print('RTN     ', var)
        elif instrucao == 'D':
            print('STOP')


'''
Função que imprime comandos para a próxima instrução.
'''

def proxima_instrucao(memoria):
    proximo = ''
    while proximo != 's':
        proximo = input('Realizar próxima instrução?\n "s" - realizar (step), "m" - verificar memória\n')
        if proximo == 'm':
            valor_hexa = input('qual posição de memória deseja imprimir (hexadecimal)? \n Digite x para memória inteira\n')
            if valor_hexa == 'x':
                print(memoria)
            else:
                print(memoria[hexadecimal_decimal(valor_hexa)])
    


'''Funções de conversão de base'''

def converte_hexadecimal(letra): #converte hexadecimal em binario
    if letra == '0':
        return '0000'
    elif letra == '1':
        return '0001'
    elif letra == '2':
        return '0010'
    elif letra == '3':
        return '0011'
    elif letra == '4':
        return '0100'
    elif letra == '5':
        return '0101'
    elif letra == '6':
        return '0110'
    elif letra == '7':
        return '0111'
    elif letra == '8':
        return '1000'
    elif letra == '9':
        return '1001'
    elif letra == 'A':
        return '1010'
    elif letra == 'B':
        return '1011'
    elif letra == 'C':
        return '1100'
    elif letra == 'D':
        return '1101'
    elif letra == 'E':
        return '1110'
    elif letra == 'F':
        return '1111'


def decimal_binario(decimal, tamanho): #converte decimal em binario
    negativo = False
    if decimal < 0:
        negativo = True
        decimal += 1
        decimal = decimal * (-1)
    binario = ''
    while decimal != 0:
        resto = decimal % 2
        decimal //= 2
        if resto == 1:
            binario += '1'
        else:
            binario += '0'
    while (len(binario) < tamanho):
        binario += '0'
    resposta = ''
    i = 1
    while i <= tamanho:
        resposta += binario[tamanho-i]
        i += 1
    binario = resposta

    if negativo:
        complemento_2 = ''
        i = 0
        while i < tamanho:
            if binario[i] == '0':
                complemento_2 += '1'
            else:
                complemento_2 += '0'
            i += 1
        return complemento_2
    return binario

def binario_decimal(binario, tamanho, complemento_2): #converte binário em decimal
    sinal = 1
    if complemento_2:
        complemento_2 = ''
        if binario[0] == '1':
            i = 0
            sinal = -1
            while i < tamanho:
                if binario[i] == '1':
                    complemento_2 += '0'
                else:
                    complemento_2 += '1'
                i += 1
            binario = complemento_2
    i = 1
    dec = 0
    while i <= tamanho:
        if binario[tamanho - i] == '1':
            dec += 2**(i - 1)
        i += 1
    if sinal == -1:
        dec += 1
    return sinal*dec


def hexadecimal_decimal(valor): #converte hexadecimal em decimal
    resposta = 0
    for i in range(len(valor)):
        decimal = binario_decimal(converte_hexadecimal(valor[i]), 4, False)
        resposta += decimal * (16**(len(valor) - i - 1))
    return resposta


def binario_hexa(valor):#converte binario em hexadecimal


    decimal = binario_decimal(valor, len(valor), False)
    i = 1
    hexa = ''
    while decimal != 0:
        resto = decimal % 16
        decimal = decimal //16
        i += 1
        if resto == 0:
            hexa += '0'
        elif resto == 1:
            hexa += '1'
        elif resto == 2:
            hexa += '2'
        elif resto == 3:
            hexa += '3'
        elif resto == 4:
            hexa += '4'
        elif resto == 5:
            hexa += '5'
        elif resto == 6:
            hexa += '6'
        elif resto == 7:
            hexa += '7'
        elif resto == 8:
            hexa += '8'
        elif resto == 9:
            hexa += '9'
        elif resto == 10:
            hexa += 'A'
        elif resto == 11:
            hexa += 'B'
        elif resto == 12:
            hexa += 'C'
        elif resto == 13:
            hexa += 'D'
        elif resto == 14:
            hexa += 'E'
        elif resto == 15:
            hexa += 'F'
    if hexa == '':
        hexa = '0'
    resposta = ''
    i = 1
    while i <= len(hexa):
        resposta += hexa[len(hexa)-i]
        i += 1
    return resposta

        
def main():
    fita = '0015702B9025400500192031C0B00AB00BD08555A0'
    imprimir_assembly(fita)
    memoria, endereco = Loader(fita)
    maquina_instrucoes(memoria, endereco, '000000000000', [0, 1])


main()
    


