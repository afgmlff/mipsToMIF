#
#   Copyright (c) 2020 Aécio Fernandes
#   MIPS to MIF por Aécio Fernandes
#   https://github.com/afgmlff
#

import time

def localiza_imediato(instrucao):                                       #funcao para localizacao de virgulas, traduzidas para posicao do imediato (apos ultima virgula)
    return [i for i, char in enumerate(instrucao) if char == ',']

def localiza_char(instrucao, ch):                                       #funcao para localizacao de caracteres
    return [i for i, char in enumerate(instrucao) if char == ch]

def localiza_parentese_aberto(instrucao):                                #funcao para localizacao de parentese aberto, para localizar o offset em casos que exista
    return [i for i, char in enumerate(instrucao) if char == '(']

def localiza_reg(instrucao):                                       #funcao para localizacao de registradores
    return [i for i, char in enumerate(instrucao) if char == '$']

def localiza_dado(instrucao):                                       #funcao para localizacao de dados no campo .data
    return [i for i, char in enumerate(instrucao) if char == ':']


def insere_li(instrucao,linha,endereco,numero):                        #funcao para tratamento de ocorrencias da instrucao "li"

    #DIVIDINDO O LI EM LUI + ori
    #LUI:

    i = localiza_reg(instrucao)                 #localizamos o registrador chamado com li, para uso futuro
    rt1 = format((dicionario_reg("$at")),'05b')  #utiliza temporariamente o registrador $at, segundo o MARS
    opcode = "001111"
    rs1 = "00000"
    i = (localiza_imediato(instrucao))
    if(numero < 0):                             #caso o imediato passado seja negativo, é necessária a conversao para complemento a 2
        numero = int(comp2_16bit(abs(num)),2)

    upper16 = format((numero >> 16), '016b')    #a parte superior dos 32 bits do número utilizado em li é usada para a instrução lui
    imm = upper16

    machineCode = opcode + rs1 + rt1 + imm      #formação do código objeto
    num = int(machineCode, 2)
    address_txt1 = address_txt - 4               #considerando que o endereço passado fora adicionado em 8, já sabendo da necessidade de duas instruções, a primeira é anterior ao endereço atual em 4 unidades
    saida_text_arq.write(format(address_txt1 , '08X') + " : " + format(num, '08X') + ";  % " + str(linha_asm) + ": lui $at, "  + upper16 + " %\n") #formatação da linha no arquivo de saida

    #ORI
    i = localiza_reg(instrucao)
    rt = ''.join(instrucao[i[0]:i[0]+3])        #mesmo raciocinio utilizado em instruções do tipo R (função apresentada posteriormente no código)
    rt1 = format((dicionario_reg(rt)), '05b')
    rs1 = format((dicionario_reg("$at")),'05b')
    opcode = "001101"
    lower16 = (format((numero & 0x0000FFFF), '016b'))  #contudo o imediato são, agora, os 16 bits menos significativos do número original
    imm2 = lower16
    machineCode = opcode + rs1 + rt1 + imm2
    num = int(machineCode, 2)
    saida_text_arq.write(format(address_txt , '08X') + " : " + format(num, '08X') + ";  % " + str(linha_asm) + ": ori " + rt + ", $at, " + lower16 + " %\n")





def localiza_label(arquivo,label):      #função de busca da label ao longo do código, para auxiliar em instruções de branches e jumps
    i = -1
    for line in arquivo:
        if (line.startswith('add ') or line.startswith('sub ') or line.startswith('and ') or line.startswith('or ') or line.startswith('xor ')
        or line.startswith('slt ') or line.startswith('addu ') or line.startswith('subu ') or line.startswith('sll ') or line.startswith('srl ')
        or line.startswith('mult ') or line.startswith('div ') or line.startswith('mfhi ') or line.startswith('mflo ') or line.startswith('clo ')
        or line.startswith('srav ') or line.startswith('sra ') or line.startswith('jalr ') or line.startswith('jr ') or line.startswith('madd ')
        or line.startswith('msubu ') or line.startswith('nor ') or line.startswith('lw ') or line.startswith('sw ') or line.startswith('lui ')
        or line.startswith('addi ') or line.startswith('andi ') or line.startswith('ori ') or line.startswith('xori ') or line.startswith('bne ')
        or line.startswith('beq ') or line.startswith('bgez ') or line.startswith('bgezal ') or line.startswith('j ') or line.startswith('jal ')):
            i += 1
        elif line.startswith('li '):  #basicamente soma +1 na contagem de linhas de instrução, exceto quando há um "li" com imediato maior que 16 bits, onde soma-se, então, duas contagens de instrução
            m = []
            m = (localiza_imediato(line))
            numero = line[m[0]+1:]
            numero = numero.strip()
            if(numero.startswith('0x')):
                numero = int(numero,16)
            elif (numero.startswith('0n')):
                numero = int(numero,2)
            else:
                numero = int(numero,10)
            if(numero > 0xFFFF):
                i += 2
            else:
                i += 1
        if line.strip().startswith(label):
            return i
        elif(line is not line):
            print ("Alguma das \"label's\" utilizadas está declarada de forma errada. Verificar código original.")
            exit()

def comp2_16bit(num):   #funcao para comp2 de um número 16-bit
    x=num
    return(bin(abs(x - (1 << 16))))

def comp2_26bit(num):   #funcao para comp2 de um número 26-bit
    x=num
    return(bin(abs(x - (1 << 26))))

def dicionario_reg(string): #dicionario de traducao dos caracteres que representam um registrador para seu valor em inteiro.
    reg = 0
    if (string.startswith('$z') or string == '$0'):
        reg = 0
    elif (string == '$at' or string == '$1,' or string == '$1 '):
        reg = 1
    elif (string == '$v0' or string == '$2,' or string == '$2 '):
        reg = 2
    elif (string == '$v1' or string == '$3,' or string == '$3 '):
        reg = 3
    elif (string == '$a0' or string == '$4,' or string == '$4 '):
        reg = 4
    elif (string == '$a1' or string == '$5,' or string == '$5 '):
        reg = 5
    elif (string == '$a2' or string == '$6,' or string == '$6 '):
        reg = 6
    elif (string == '$a3' or string == '$7,' or string == '$7 '):
        reg = 7
    elif (string == '$t0' or string == '$8,' or string == '$8 '):
        reg = 8
    elif (string == '$t1' or string == '$9,' or string == '$9 '):
        reg = 9
    elif (string == '$t2' or string == '$10'):
        reg = 10
    elif (string == '$t3' or string == '$11'):
        reg = 11
    elif (string == '$t4' or string == '$12'):
        reg = 12
    elif (string == '$t5' or string == '$13'):
        reg = 13
    elif (string == '$t6' or string == '$14'):
        reg = 14
    elif (string == '$t7' or string == '$15'):
        reg = 15
    elif (string == '$s0' or string == '$16'):
        reg = 16
    elif (string == '$s1' or string == '$17'):
        reg = 17
    elif (string == '$s2' or string == '$18'):
        reg = 18
    elif (string == '$s3' or string == '$19'):
        reg = 19
    elif (string == '$s4' or string == '$20'):
        reg = 20
    elif (string == '$s5' or string == '$21'):
        reg = 21
    elif (string == '$s6' or string == '$22'):
        reg = 22
    elif (string == '$s7' or string == '$23'):
        reg = 23
    elif (string == '$t8' or string == '$24'):
        reg = 24
    elif (string == '$t9' or string == '$25'):
        reg = 25
    elif (string == '$k0' or string == '$26'):
        reg = 26
    elif (string == '$k1' or string == '$27'):
        reg = 27
    elif (string == '$gp' or string == '$28'):
        reg = 28
    elif (string == '$sp' or string == '$29'):
        reg = 29
    elif (string == '$fp' or string == '$30'):
        reg = 30
    elif (string == '$ra' or string == '$31'):
        reg = 31
    return reg


def transforma_tipoR (instrucao):
    i = localiza_reg(instrucao)
    # i[] é um vetor que guarda TODAS as ocorrencias de "$". Logo, seu tamanho equivale ao numero de registradores da funcao.
    #Instruções com 3 Registradores como parâmetros
    if len(i) == 3:
        rd = ''.join(instrucao[i[0]:i[0]+3])    #localiza-se a ocorrencia do caractere "$" e, então, busca-se ele e os dois próximos caracteres para tradução
        rs = ''.join(instrucao[i[1]:i[1]+3])
        rt = ''.join(instrucao[i[2]:i[2]+3])
        rs1 = format((dicionario_reg(rs)),'05b')  #tradução do valor, formatado para um número em binário com 5 bits
        rt1 = format((dicionario_reg(rt)),'05b')
        rd1 = format((dicionario_reg(rd)),'05b')
#        print(rs1)
#        print(rt1)
#        print(rd1)
        opcode = "000000"
        shamt = "00000"

        if(instrucao.startswith('add ')):   #valores registrados de func para as instruções
            func = "100000"
        elif(instrucao.startswith('sub ')):
            func = "100010"
        elif(instrucao.startswith('and ')):
            func = "100100"
        elif(instrucao.startswith('or ')):
            func = "100101"
        elif(instrucao.startswith('nor ')):
            func = "100111"
        elif(instrucao.startswith('xor ')):
            func = "100110"
        elif(instrucao.startswith('srav ')):
            func = "000111"
        elif(instrucao.startswith('slt ')):
            func = "101010"

    #Instruções com 2 registradores como parâmetros
    elif len(i) == 2: #segue o mesom raciocinio acima, com a atribuicao de algum dos registradores para o valor tabelado no manual, dependendo da instrucao
        if(instrucao.startswith('mult ')):
            opcode = "000000"
            rd = "00000"
            shamt = "00000"
            func = "011000"
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            rd1 = rd

        elif(instrucao.startswith('div ')):
            opcode = "000000"
            rd = "00000"
            shamt = "00000"
            func = "011010"
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            rd1 = rd

        elif(instrucao.startswith('madd ')):
            opcode = "011100"
            rd = "00000"
            shamt = "00000"
            func = "000000"
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            rd1 = rd

        elif(instrucao.startswith('msubu ')):  #TESTAR
            opcode = "011100"
            rd = "00000"
            shamt = "00000"
            func = "000101"
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            rd1 = rd

        elif(instrucao.startswith('clo ')):  #TESTAR
            opcode = "011100"
            rt = "00000"
            shamt = "00000"
            func = "100001"
            rd = ''.join(instrucao[i[0]:i[0]+3])
            rs = ''.join(instrucao[i[1]:i[1]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rd1 = format((dicionario_reg(rd)),'05b')
            rt1 = rt

        elif(instrucao.startswith('jalr ')): #formato 2
            opcode = "000000"
            rt = "00000"
            shamt = "00000"
            func = "001001"
            rd = ''.join(instrucao[i[0]:i[0]+3])
            rs = ''.join(instrucao[i[1]:i[1]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = rt
            rd1 = format((dicionario_reg(rd)),'05b')

        elif(instrucao.startswith('sll ')):
            opcode = "000000"
            rs = "00000"
            func = "000000"
            rd = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rd1 = format((dicionario_reg(rd)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            rs1 = rs

            i = (localiza_imediato(instrucao))
            numero = instrucao[i[1]+1:]
            numero = numero.strip()

            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                shamt = format(num,'05b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                shamt = format(num,'05b')

            else:
                num = int(numero.strip(), 10)
                shamt = format(num,'05b')

        elif(instrucao.startswith('srl ')):
            opcode = "000000"
            rs = "00000"
            func = "000010"
            rd = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rd1 = format((dicionario_reg(rd)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            rs1 = rs

            i = (localiza_imediato(instrucao))
            numero = instrucao[i[1]+1:]
            numero = numero.strip()

            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                shamt = format(num,'05b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                shamt = format(num,'05b')

            else:
                num = int(numero.strip(), 10)
                shamt = format(num,'05b')

        elif(instrucao.startswith('sra ')):
            opcode = "000000"
            rs = "00000"
            func = "000011"
            rd = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rd1 = format((dicionario_reg(rd)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            rs1 = rs

            i = (localiza_imediato(instrucao))
            numero = instrucao[i[1]+1:]
            numero = numero.strip()

            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                shamt = format(num,'05b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                shamt = format(num,'05b')

            else:
                num = int(numero.strip(), 10)
                shamt = format(num,'05b')

    #Instruções com 1 registrador como parâmetro
    elif len(i) == 1:
        if(instrucao.startswith('jr ')):
            opcode = "000000"
            rd = "00000"
            rt = "00000"
            shamt = "00000"
            func = "001000"
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = rt
            rd1 = rd

        elif(instrucao.startswith('jalr ')):
            opcode = "000000"
            rd = "11111"
            rt = "00000"
            shamt = "00000"
            func = "001001"
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = rt
            rd1 = rd

        elif(instrucao.startswith('mfhi ')):
            opcode = "000000"
            rs = "00000"
            rt = "00000"
            shamt = "00000"
            func = "010000"
            rd = ''.join(instrucao[i[0]:i[0]+3])
            rd1 = format((dicionario_reg(rd)),'05b')
            rt1 = rt
            rs1 = rs

        elif(instrucao.startswith('mflo ')):
            opcode = "000000"
            rs = "00000"
            rt = "00000"
            shamt = "00000"
            func = "010010"
            rd = ''.join(instrucao[i[0]:i[0]+3])
            rd1 = format((dicionario_reg(rd)),'05b')
            rt1 = rt
            rs1 = rs


    machineCode = opcode + rs1 + rt1 + rd1 + shamt + func
    num = int(machineCode, 2)
    return format(num, '08X')  #troquei pra X maiusculo para imprimir em maiusculo o hex, verificar em versoes





def transforma_tipoI (instrucao):
    i = localiza_reg(instrucao)

    #Instruções com 3 Registradores como parâmetros
    if len(i) == 2:
        rt = ''.join(instrucao[i[0]:i[0]+3])
        rs = ''.join(instrucao[i[1]:i[1]+3])
        rs1 = format((dicionario_reg(rs)),'05b')
        rt1 = format((dicionario_reg(rt)),'05b')

        if(instrucao.startswith('lw ')):
            opcode = "100011"
            i = (localiza_imediato(instrucao))      #localiza a posição das virgulas na instrucao.
            j = (localiza_parentese_aberto(instrucao))#localiza a posicao do parentese do ultimo argumento
            numero = instrucao[i[0]+1:j[0]] #o numero do offset está entre a ultima virgula e o parentese
            numero = numero.strip()     #remove espacos em branco
            if (numero.startswith('0b')):  #trata binario, hexa ou decimal
                num = int(numero.strip(), 2)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            else:
                num = int(numero.strip(), 10)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

        elif(instrucao.startswith('sw ')): #mesmo raciocício acima
            opcode = "101011"
            i = (localiza_imediato(instrucao))
            j = (localiza_parentese_aberto(instrucao))
            numero = instrucao[i[0]+1:j[0]]
            numero = numero.strip()
            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            else:
                num = int(numero.strip(), 10)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

        elif(instrucao.startswith('addi ')):
            opcode = "001000"
            i = (localiza_imediato(instrucao))
            numero = instrucao[i[1]+1:]
            numero = numero.strip()
            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            else:
                num = int(numero.strip(), 10)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

        elif(instrucao.startswith('andi ')):
            opcode = "001100"
            i = (localiza_imediato(instrucao))
            numero = instrucao[i[1]+1:]
            numero = numero.strip()
            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            else:
                num = int(numero.strip(), 10)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

        elif(instrucao.startswith('ori ')):
            opcode = "001101"
            i = (localiza_imediato(instrucao))
            numero = instrucao[i[1]+1:]
            numero = numero.strip()
            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            else:
                num = int(numero.strip(), 10)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

        elif(instrucao.startswith('xori ')):
            opcode = "001110"
            i = (localiza_imediato(instrucao))
            numero = instrucao[i[1]+1:]
            numero = numero.strip()
            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            else:
                num = int(numero.strip(), 10)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

    elif len(i) == 1: #para apenas um registrador, o outro é atribuido um valor tabelado no manual por instrução.
        rt = ''.join(instrucao[i[0]:i[0]+3])
        rt1 = format((dicionario_reg(rt)),'05b')

        if(instrucao.startswith('lui ')):
            opcode = "001111"
            rs1 = "00000"
            i = (localiza_imediato(instrucao))
            numero = instrucao[i[0]+1:]
            numero = numero.strip()
            if (numero.startswith('0b')):
                num = int(numero.strip(), 2)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            elif (numero.startswith('0x')):
                num = int(numero.strip(), 16)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')

            else:
                num = int(numero.strip(), 10)
                if(num < 0):
                    num = int(comp2_16bit(abs(num)),2)
                imm = format(num,'016b')




    machineCode = opcode + rs1 + rt1 + imm
    num = int(machineCode, 2)
    return format(num, '08X')    #retorna a concatenação dos atributos que compoe o código, formatado para hexadecimal 8 caracteres.


def transforma_jump_branch(instrucao, linha, endereco):
    k = localiza_imediato(instrucao)        #reaproveitando o metodo de localizar imediato para localizar a label na instrucao
    i = localiza_reg(instrucao)
    if (k != []):
        label = (instrucao[k[len(k)-1]+1:].strip()) #instrucao deve ter, ao menos, 1 registrador como operando; jumps sao realizados de outra maneira.
#        print(linha)
        arquivo_temp = open(arquivo_nome, 'r')
        j = localiza_label(arquivo_temp,label + ":")
#        print(j)
        offset = (j - (linha))  #começa a contar a partir da próxima linha, offset é a distancia entre as linhas em contagem de instruções.
        if(j < linha):
            offset = comp2_16bit(abs(offset))[2:]
        else:
            offset = format(offset,'016b')

    #    print(offset)
        if len(i) == 2:   #formatação para 2 registradores, seguindo raciocínio de instrucoes do tipo I
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rt = ''.join(instrucao[i[1]:i[1]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            rt1 = format((dicionario_reg(rt)),'05b')
            if (line.startswith('beq ')):
                opcode = "000100"
            elif (line.startswith('bne ')):
                opcode = "000101"

        elif len(i) == 1: #formatação para 1 registrador
            rs = ''.join(instrucao[i[0]:i[0]+3])
            rs1 = format((dicionario_reg(rs)),'05b')
            if (line.startswith('bgez ')):
                rt1 = "00001"
                opcode = "000001"
            elif (line.startswith('bgezal ')):
                rt1 = "10001"
                opcode = "000001"

        machineCode = opcode + rs1 + rt1 + offset
        num = int(machineCode, 2)
        return format(num, '08X')

    elif(k == []):
        if (line.startswith('j ')):
            opcode = "000010"
            label = line[1:].strip()
            j = []
            arquivo_temp = open(arquivo_nome, 'r')
            j = localiza_label(arquivo_temp,label + ":")
    #        print(j)
            offset = (j - (linha) + 1)  #começa a contar a partir da próxima linha
            imediato = (endereco + (offset*4)) >> 2 #trabalhando-se com jumps, o valor do endereço passa a ser absoluto, com um shift de 2 bits segundo o manual
            imediato = format(imediato,'026b')      #maiores detalhes estão especificados no relatório.
            machineCode = opcode + imediato
            num = int(machineCode, 2)
            return format(num, '08X')

        elif (line.startswith('jal ')):
            opcode = "000011"
            label = line[3:].strip()
            j = []
            arquivo_temp = open(arquivo_nome, 'r')
            j = localiza_label(arquivo_temp,label + ":")
    #        print(j)
            offset = (j - (linha) + 1)  #começa a contar a partir da próxima linha
            imediato = (endereco + (offset*4)) >> 2
            imediato = format(imediato,'026b')
            machineCode = opcode + imediato
            num = int(machineCode, 2)
            return format(num, '08X')







arquivo_nome = input('Insira o nome do arquivo (ex.: exemplo.asm): ')

with open(arquivo_nome) as fp:                  #busca os indexes dos campos de dados e texto para ver qual é processado primeiro
    for i, line in enumerate(fp):
        if line.strip().startswith('.data'):
            data_index = i
        elif line.strip().startswith('.text'):
            text_index = i

try:
    arquivo = open(arquivo_nome, 'r')
except OSError:
    print ("Arquivo nao encontrado. Reinicie a aplicacao e insira um nome valido.")
    exit()

saida_data = arquivo_nome[:len(arquivo_nome)-4] + "_data.mif"

saida_data_arq = open(saida_data, 'w')  #criação do arquivo de saida com o nome do de entrada, mudando o final e o formato para _data.mif

saida_text = arquivo_nome[:len(arquivo_nome)-4] + "_text.mif"

saida_text_arq = open(saida_text, 'w') #criação do arquivo de saida com o nome do de entrada, mudando o final e o formato para _text.mif

if(data_index<text_index): #caso o index de .data seja menor, o primeiro processamento é em dados
    cabecalho = "DEPTH = 16384;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n"

    saida_data_arq.write(cabecalho)

    address_data = 0x10010000 - 4
    while True:
        line = arquivo.readline()
        if not line:
            break
        j = localiza_dado(line) #apos a ocorrencia de ":", o que vem são dados
        if(j != []):
            dados = (line[j[0]+7:].strip().split(',')) #cria um vetor para os dados, separados por vírgula
            it1 = 0


            for item in dados:  #loop de escrita dos dados com endereços no arquivo de saida
                address_data += 4
 #           print(item)
                if (item.strip().startswith('0b')):  #verifica binario, hexa ou decimal
                    dados[it1] = int(item.strip(), 2)

                elif (item.strip().startswith('0x')):
                    dados[it1] = int(item.strip(), 16)

                else:
                    dados[it1] = int(item.strip(), 10)
                saida_data_arq.write(format(address_data, '08X') + ' : ' + format(dados[it1],'08X') + ";\n")  #vai pro arquivo de saida
                it1 += 1

        if(line.strip().startswith('.text')):  #caso chege na area .text, passa para a proxima parte da execucao
                break

    saida_data_arq.write("\nEND;")
#count = 0
    linha = -1
    linha_asm = 0
    address_txt = 0x00400000 - 4
    cabecalho2 = "DEPTH = 4096;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n"
    saida_text_arq.write(cabecalho2)
#rotina para imprimir linha por linha
    while True:

        line = arquivo.readline()
        if not line:
            saida_text_arq.write("\nEND;")
            break

        linha_asm += 1

        #identifica qual instrucao estamos lidando
        if (line.startswith('add ') or line.startswith('sub ') or line.startswith('and ') or line.startswith('or ') or line.startswith('xor ')
        or line.startswith('slt ') or line.startswith('addu ') or line.startswith('subu ') or line.startswith('sll ') or line.startswith('srl ')
        or line.startswith('mult ') or line.startswith('div ') or line.startswith('mfhi ') or line.startswith('mflo ') or line.startswith('clo ')
        or line.startswith('srav ') or line.startswith('sra ') or line.startswith('jalr ') or line.startswith('jr ') or line.startswith('madd ')
        or line.startswith('msubu ') or line.startswith('nor ')):
            address_txt += 4
            linha += 1
            machine = transforma_tipoR(line) #chama formatacao para tipo R
            saida_text_arq.write(format(address_txt , '08X') + " : " + machine + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n") #escreve o retorno formatado no arquivo de saida

        elif (line.startswith('lw ') or line.startswith('sw ') or line.startswith('lui ') or line.startswith('addi ') or line.startswith('andi ')
        or line.startswith('ori ') or line.startswith('xori ')):
            address_txt += 4
            linha += 1
            machine = transforma_tipoI(line) #chama formatacao para tipo R
            saida_text_arq.write(format(address_txt , '08X') + " : " + machine + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n")

        elif (line.startswith('bne ') or line.startswith('beq ') or line.startswith('bgez ') or line.startswith('bgezal ') or line.startswith('j ') or line.startswith('jal ') ):
            start = time.time()
            address_txt += 4
            linha += 1
            machine = transforma_jump_branch(line, linha, address_txt) #chama formatacao para tipo branches e jumps
            saida_text_arq.write(format(address_txt , '08X') + " : " + machine + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n")
            stop = time.time()

        elif (line.startswith('li ')):
         #caso especial: pseudoinstrucao "li"

            m = []
            m = (localiza_imediato(line))
            numero = line[m[0]+1:]
            numero = numero.strip()
            if(numero.startswith('0x')):
                numero = int(numero,16)
            elif (numero.startswith('0n')):
                numero = int(numero,2)
            else:
                numero = int(numero,10)
            if(numero > 0xFFFF):    #primeiro passo: verificar o tamanho do imediato. se for maior que 16 bits, chama a função do comeco do codigo para insercao das outras duas instrucoes no lugar
                address_txt += 8
                linha += 1
                insere_li(line, linha, address_txt, numero)
            else: #caso seja menor, basta tratar como "addiu", seguindo a formataçao das instrucoes do tipo I, trocando o opcode para addiu.
                i = []
                n = []
                n = localiza_reg(line)
                address_txt += 4
                rt = ''.join(line[n[0]:n[0]+3])
                rt1 = format((dicionario_reg(rt)),'05b')
                rs1 = "00000"
                opcode = "001001"
                i = (localiza_imediato(line))
                numero = line[i[0]+1:]
                numero = numero.strip()
                if (numero.startswith('0b')):
                    num = int(numero.strip(), 2)
                    if(num < 0):
                        num = int(comp2_16bit(abs(num)),2)
                    imm = format(num,'016b')

                elif (numero.startswith('0x')):
                    num = int(numero.strip(), 16)
                    if(num < 0):
                        num = int(comp2_16bit(abs(num)),2)
                    imm = format(num,'016b')

                else:
                    num = int(numero.strip(), 10)
                    if(num < 0):
                        num = int(comp2_16bit(abs(num)),2)
                    imm = format(num,'016b')

                machineCode = opcode + rs1 + rt1 + imm
                num = int(machineCode, 2)
                saida_text_arq.write(format(address_txt , '08X') + " : " + format(num, '08X') + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n")

else: #caso o campo text venha antes do data, faz a mesma coisa que a condição acima porém na ordem inversa.
    #count = 0
    linha = -1
    linha_asm = 0
    address_txt = 0x00400000 - 4
    cabecalho2 = "DEPTH = 4096;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n"
    saida_text_arq.write(cabecalho2)
    #rotina para imprimir linha por linha
    while True:

        line = arquivo.readline()
        if not line:
            break

        linha_asm += 1

        if (line.startswith('add ') or line.startswith('sub ') or line.startswith('and ') or line.startswith('or ') or line.startswith('xor ')
        or line.startswith('slt ') or line.startswith('addu ') or line.startswith('subu ') or line.startswith('sll ') or line.startswith('srl ')
        or line.startswith('mult ') or line.startswith('div ') or line.startswith('mfhi ') or line.startswith('mflo ') or line.startswith('clo ')
        or line.startswith('srav ') or line.startswith('sra ') or line.startswith('jalr ') or line.startswith('jr ') or line.startswith('madd ')
        or line.startswith('msubu ') or line.startswith('nor ')):
            address_txt += 4
            linha += 1
            machine = transforma_tipoR(line)
            saida_text_arq.write(format(address_txt , '08X') + " : " + machine + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n")

        elif (line.startswith('lw ') or line.startswith('sw ') or line.startswith('lui ') or line.startswith('addi ') or line.startswith('andi ')
        or line.startswith('ori ') or line.startswith('xori ')):
            address_txt += 4
            linha += 1
            machine = transforma_tipoI(line)
            saida_text_arq.write(format(address_txt , '08X') + " : " + machine + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n")

        elif (line.startswith('bne ') or line.startswith('beq ') or line.startswith('bgez ') or line.startswith('bgezal ') or line.startswith('j ') or line.startswith('jal ') ):
            address_txt += 4
            linha += 1
            machine = transforma_jump_branch(line, linha, address_txt)
            saida_text_arq.write(format(address_txt , '08X') + " : " + machine + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n")

        elif (line.startswith('li ')):
            m = []
            m = (localiza_imediato(line))
            numero = line[m[0]+1:]
            numero = numero.strip()
            if(numero.startswith('0x')):
                numero = int(numero,16)
            elif (numero.startswith('0n')):
                numero = int(numero,2)
            else:
                numero = int(numero,10)
            if(numero > 0xFFFF):
                address_txt += 8
                linha += 1
                insere_li(line, linha, address_txt, numero)
            else:
                i = []
                n = []
                n = localiza_reg(line)
                address_txt += 4
                rt = ''.join(line[n[0]:n[0]+3])
                rt1 = format((dicionario_reg(rt)),'05b')
                rs1 = "00000"
                opcode = "001001"
                i = (localiza_imediato(line))
                numero = line[i[0]+1:]
                numero = numero.strip()
                if (numero.startswith('0b')):
                    num = int(numero.strip(), 2)
                    if(num < 0):
                        num = int(comp2_16bit(abs(num)),2)
                    imm = format(num,'016b')

                elif (numero.startswith('0x')):
                    num = int(numero.strip(), 16)
                    if(num < 0):
                        num = int(comp2_16bit(abs(num)),2)
                    imm = format(num,'016b')

                else:
                    num = int(numero.strip(), 10)
                    if(num < 0):
                        num = int(comp2_16bit(abs(num)),2)
                    imm = format(num,'016b')

                machineCode = opcode + rs1 + rt1 + imm
                num = int(machineCode, 2)
                saida_text_arq.write(format(address_txt , '08X') + " : " + format(num, '08X') + ";  % " + str(linha_asm) + ": " + line[0:(len(line)-1)] + " %\n")
#    print(linha)
        if(line.strip().startswith('.data')):
            saida_text_arq.write("\nEND;")
            break

    cabecalho = "DEPTH = 16384;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n"

    saida_data_arq.write(cabecalho)

    address_data = 0x10010000 - 4
    while True:
        line = arquivo.readline()
        if not line:
            break
        j = localiza_dado(line)
        if(j != []):
            dados = (line[j[0]+7:].strip().split(','))
            it1 = 0


            for item in dados:
                address_data += 4
 #           print(item)
                if (item.strip().startswith('0b')):
                    dados[it1] = int(item.strip(), 2)

                elif (item.strip().startswith('0x')):
                    dados[it1] = int(item.strip(), 16)

                else:
                    dados[it1] = int(item.strip(), 10)
                saida_data_arq.write(format(address_data, '08X') + ' : ' + format(dados[it1],'08X') + ";\n")  #vai pro arquivo de saida
                it1 += 1

        if(line.strip().startswith('.text')):
                break

    saida_data_arq.write("\nEND;")


#fim da rotina

saida_text_arq.close
saida_data_arq.close
arquivo.close

