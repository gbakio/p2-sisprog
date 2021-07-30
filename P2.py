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
    i = 0
    while i < 4:
        endereco += converte_hexadecimal(fita[i])
        i += 1
    i = 4
    endereco_inicial = endereco
    
    while True:
        comando = converte_hexadecimal(fita[i])
        if comando == '1100' or comando == '1101' or comando == '1010':
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
    reg = ['000000000000']
    flags = [0, 1]
    '''máquina de instruções'''
    while True:
        comando = memoria[endereco]
        if comando != '1100' and comando != '1101':
        
            dados = memoria[endereco + 1] + memoria[endereco + 2] + memoria[endereco + 3]
            if comando == '0000' or comando == '0001' or comando == '0010':
                endereco = funcao_desvio(comando, dados, endereco, flags)
            elif comando == '0011' or comando == '0100' or comando == '0101' or comando == '0110':
                reg = funcao_aritmetica(comando, dados, reg, flags)
            elif comando == '0111':
                funcao_load(dados, flags, memoria)
            elif comando == '1000':
                funcao_store(dados, reg, memoria)
            elif comando == '1001':
                maquina_instrucoes(memoria, dados)
            else:
                break

        else:
            if comando == '1100':
                return
            elif comando == '1101':
                funcao_stop()

            
def funcao_store(dados, reg, memoria):
    memoria[dados] = reg[0] + reg[1] + reg[2] + reg[3]
    memoria[dados + 1] = reg[4] + reg[5] + reg[6] + reg[7]
    memoria[dados + 2] = reg[8] + reg[9] + reg[10] + reg[11]
    
def funcao_load(dados, flags, memoria):
    valor = memoria[dados]+memoria[dados + 1] + memoria[dados + 2]
    if complemento_2_decimal(valor, 12) < 0:
        flags = [1, 0]
    elif complemento_2_decimal(valor, 12) == 0:
        flags = [0, 1]
    else:
        flags = [0, 0]
    return valor
    
def funcao_aritmetica(comando, dados, reg, flags):
    return(ULA(comando, reg, dados))

def ULA(comando, reg, dados):
    reg_dec = complemento_2_decimal(reg, 32)
    dados_dec = complemento_2_decimal(dados, 12)
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
    retorno_binario = decimal_complemento_2(retorno, 32)
    return(retorno_binario)
        
def complemento_2_decimal(binario, tamanho):
    sinal = 1
    if binario[0] == '1':
        i = 0
        sinal = -1
        while i < tamanho:
            if binario[i] == '1':
                binario[i] = '0'
    i = 0
    while i <= tamanho:
        if binario[tamanho - i] == '1':
            dec += 2**(32 - i)
    if sinal == -1:
        dec += 1
    return sinal*dec

def decimal_complemento_2(decimal, tamanho):
    negativo = False
    if decimal < 0:
        negativo = True
        decimal += 1
        decimal = decimal * (-1)
    i = tamanho
    binario = ''
    while i >= 0:
        if 2**i <= decimal:
            binario += '1'
        else:
            binario += '0'
        i -=  1
    if negativo:
        i = 0
        while i < tamanho:
            if binario[i] == '0':
                binario[i] = '1'
            else:
                binario[i] = '0'
    return binario

    
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