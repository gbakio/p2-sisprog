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

def maquina_instrucoes(memoria, endereco):
    reg = '000000000000'
    flags = [0, 1]
    '''máquina de instruções'''
    while True:
        print(endereco)
        comando = memoria[endereco]
        if comando != '1100' and comando != '1101':
            
            dados = memoria[endereco + 1] + memoria[endereco + 2] + memoria[endereco + 3]
            print('Próxima Instrução:')
            imprime_instrucao(binario_hexa(comando), binario_hexa(dados))
            proxima_instrucao(memoria)
            if comando == '0000' or comando == '0001' or comando == '0010':
                endereco = funcao_desvio(comando, dados, endereco, flags)
            elif comando == '0011' or comando == '0100' or comando == '0101' or comando == '0110':
                reg = funcao_aritmetica(comando, dados, reg, flags)
                endereco += 4
            elif comando == '0111':
                funcao_load(dados, flags, memoria)
                endereco += 4
            elif comando == '1000':
                funcao_store(dados, reg, memoria)
                endereco += 4
            elif comando == '1001':
                maquina_instrucoes(memoria, dados)
                endereco += 4
            else:
                break

        else:
            dados = ''
            if comando == '1100':
                return
            elif comando == '1101':
                funcao_stop()
                endereco += 2
        print('Instrução Realizada:')
        imprime_instrucao(binario_hexa(comando), binario_hexa(dados))
        print('Valor do registrador:', reg)
        
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
    
def funcao_stop():
    while True
        continua = input('Máquina de instruções em pausa, caso deseje continuar de onde parou digite c')
        if continua == 'c':
            return
        

            
def funcao_store(dados_bin, reg, memoria):
    dados = binario_decimal(dados_bin, 12, False)
    memoria[dados] = reg[0] + reg[1] + reg[2] + reg[3]
    memoria[dados + 1] = reg[4] + reg[5] + reg[6] + reg[7]
    memoria[dados + 2] = reg[8] + reg[9] + reg[10] + reg[11]
    
def funcao_load(dados_bin, flags, memoria):
    dados = binario_decimal(dados_bin, 12, False)
    valor = memoria[dados]+memoria[dados + 1] + memoria[dados + 2]
    if binario_decimal(valor, 12, True) < 0:
        flags = [1, 0]
    elif binario_decimal(valor, 12, True) == 0:
        flags = [0, 1]
    else:
        flags = [0, 0]
    return valor
    
def funcao_aritmetica(comando, dados, reg, flags):
    return(ULA(comando, reg, dados))

def ULA(comando, reg, dados):
    reg_dec = binario_decimal(reg, 12, True)
    dados_dec = binario_decimal(dados, 12, True)
    if comando == '0011':
        retorno = dados_dec + reg_dec
    if comando == '0100':
        retorno = reg_dec - dados_dec
    if comando == '0101':
        retorno = dados_dec*reg_dec
    if comando == '0110':
        retorno = dados_dec // reg_dec
    if retorno == 0:
        flags = [0, 1]
    elif retorno < 0:
        flags = [1, 0]
    else:
        flags = [0, 0]
    retorno_binario = decimal_binario(retorno, 12)
    return(retorno_binario)
        

    
def funcao_desvio(comando, dados, endereco,  flags):

    if comando == '0000':
        return dados
    if comando == '0001':
        if flags[1] == '1':
            return dados
        else:
            return endereco
    if comando == '0010':
        if flags[0] == '1':
            return dados
        else:
            return endereco

            
def simula_memoria():
    return [0]*4096



    
def imprimir_assembly(fita):
    i = 0
    var = fita[1] + fita[2] + fita[3]
    print('1-          ORG     ', var)
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

'''Funções de conversão'''

def converte_hexadecimal(letra):
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


def decimal_binario(decimal, tamanho):
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
        i = 0
        while i < tamanho:
            if binario[i] == '0':
                binario[i] = '1'
            else:
                binario[i] = '0'
    return binario

def binario_decimal(binario, tamanho, complemento_2):
    sinal = 1
    if complemento_2:
        if binario[0] == '1':
            i = 0
            sinal = -1
            while i < tamanho:
                if binario[i] == '1':
                    binario[i] = '0'
    i = 1
    dec = 0
    while i <= tamanho:
        if binario[tamanho - i] == '1':
            dec += 2**(i - 1)
        i += 1
    if sinal == -1:
        dec += 1
    return sinal*dec


def hexadecimal_decimal(valor):
    resposta = 0
    for i in range(len(valor)):
        decimal = binario_decimal(converte_hexadecimal(valor[i]), 4, False)
        resposta += decimal * (16**(len(valor) - i - 1))
    return resposta


def binario_hexa(valor):


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
    resposta = ''
    i = 1
    while i <= len(hexa):
        resposta += hexa[len(hexa)-i]
        i += 1
    return resposta

        
def main():
    fita = '029E72A732A882A9029ED0B010B025B003A0'
    imprimir_assembly(fita)
    memoria, endereco = Loader(fita)
    maquina_instrucoes(memoria, endereco)



main()
