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
    org = 1011
    return = 1100
    stop = 1101
'''


def Loader (fita):
    endereco = ''
    i = 0
    while i < 4:
        endereco += converte_hexadecimal(fita[i])
        i += 1
    i = 4
    instrucoes = ['Z']*100
    j = 0
    while True:
        comando = converte_hexadecimal(fita[i])
        if comando == '1100' or comando == '1101':
            instrucoes[j] = comando + converte_hexadecimal(fita[i+1])
            i += 2
        if comando == '1010':
            break
        else:
            instrucoes[j] = comando + converte_hexadecimal(fita[i+1]) + converte_hexadecimal(fita[i+2]) + converte_hexadecimal(fita[i+3])
            i += 4
        j += 1
    return instrucoes

def maquina_instrucoes(instrucoes, endereco):
    memoria = simula_memoria()
    i = 0
    reg = False
    flags = [0, 0]
    endereco_inicio = endereco
    while instrucoes[i] != 'Z':
        j = 0
        while j != '':
            memoria[endereco] = instrucoes[i][j] + instrucoes[i][j+1] + instrucoes[i][j+2] + instrucoes[i][j+3]
            endereco += 1
            j += 4
        i += 1
    endereco_fim = endereco
    endereco = endereco_inicio
    while endereco < endereco_fim:
        comando = memoria[endereco]
        if comando != '1100' and comando != '1101':
        
            dados = memoria[endereco+1] + memoria[endereco + 2] + memoria[endereco + 3] + memoria[endereco+4]
            if comando == '0000' or comando == '0001' or comando == '0010':
                endereco = funcao_desvio(comando, dados, endereco, flags, i)
            elif comando == '0011' or comando == '0100' or comando == '0101' or comando == '0110':
                funcao_aritmetica(comando, dados, reg)
            '''elif comando == '0111' or comando == '1000':
                funcao_memoria(comando, dados, reg, flags)
            elif comando == '1001':
                pass
            else:
                break'''
            

def funcao_aritmetica(comando, dados, reg):
    if comando == '0011':
        soma = ULA(comando, reg, dados)

def ULA(comando, reg, dados):
    if comando == '0011':
        reg = int(dados)
        reg_dec = 0
        
            
    
        


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
