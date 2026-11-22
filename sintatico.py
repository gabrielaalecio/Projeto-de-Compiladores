from enum import Enum
class Status(Enum):
    SHIFT = "S"
    REDUZ = "R"
    DESVIO = "D"
    SUCESSO = "A"

class Simbolo():
    def __init__(self, key, valor):
        self.key = key
        self.valor = valor

class ReducaoGramatica():
    def __init__(self, num_gramatica, filhos, pos):
        self.num_gramatica = num_gramatica
        self.filhos = filhos
        self.pos = pos

def gerar_codigo(reducao):
    relacao = {
            22: "CPIG",
            23: "CDES",
            24: "CMAI",
            25: "CPMI",
            26: "CPMA",
            27: "CPME"
        }

    operacoes = {
        37: "SOMA",
        40: "MULT",
        41: "DIVI",
        42: "SUBT"
    }
    
    endereco = {}
    final = ["INPP"]
    rotulos = [0]
    marca = []
    carregar_depois = None
    nomes_decl = []  

    def novo_rotulo():
        rotulos[0] += 1
        return f"L{rotulos[0]}"

    def cria_end(nome):
        if nome in endereco:
            raise ValueError(
                f"Variável '{nome}' declarada mais de uma vez."
            )
        endereco[nome] = len(endereco)

    def busca_end(nome):
        if nome not in endereco:
            raise ValueError(
                f"Variável '{nome}' não declarada."
            )
        return endereco[nome]
    
    def decompor_filhos(red, lista):
        def n_nt(r):
            return sum(1 for f in r.filhos if isinstance(f, str))

        pendentes = n_nt(red)  
        atual = red.pos                  
        while pendentes != 0:
            atual -= 1
            pendentes = pendentes - 1 + n_nt(lista[atual])
        return atual

    
    for i in reducao:
        marca.append(len(final))
        match i.num_gramatica:
                case 4: 
                    for nome in [i.filhos[1][1]] + nomes_decl[::-1]:
                        cria_end(nome)
                    nomes_decl.clear()
                case 5: 
                    nomes_decl.append(i.filhos[1][1])
                    final.append("ALME 1") 
                case 6:
                    final.append("ALME 1")
                case 15: 
                    final.append(f"ARMZ {busca_end(i.filhos[-1][1])}")   
                case 32:
                    final.append(f"CRVL {busca_end(i.filhos[0][1])}")
                case 33:
                    final.append(f"CRCT {i.filhos[0][1]}")
                case 12:
                    k = i.pos
                    falso_ini = decompor_filhos(reducao[k - 1], reducao)
                    corpo_ini = decompor_filhos(reducao[falso_ini - 1], reducao)
                    cond_ini = decompor_filhos(reducao[corpo_ini - 1], reducao)
                    tem_else = reducao[k - 1].num_gramatica == 16 

                    l_fim = novo_rotulo()
                    final.append(f"{l_fim}:")
                    if tem_else:
                        l_else = novo_rotulo()
                        pos_else = marca[falso_ini]
                        final[pos_else:pos_else] = [f"DSVI {l_fim}", f"{l_else}:"]
                        final.insert(marca[corpo_ini], f"DSVF {l_else}")            
                    else:
                        final.insert(marca[corpo_ini], f"DSVF {l_fim}")          
                case 13:
                    k = i.pos
                    corpo_ini = decompor_filhos(reducao[k - 1], reducao)
                    cond_ini = decompor_filhos(reducao[corpo_ini - 1], reducao)

                    l_ini, l_fim = novo_rotulo(), novo_rotulo()
                    final += [f"DSVI {l_ini}", f"{l_fim}:"]         
                    final.insert(marca[corpo_ini], f"DSVF {l_fim}") 
                    final.insert(marca[cond_ini], f"{l_ini}:") 
                case 14:
                    final.append(f"CRVL {endereco[i.filhos[2][1]]}")
                    final.append("IMPR")
                case 22 | 23 | 24 | 25 | 26 | 27 :
                    carregar_depois = relacao[i.num_gramatica]
                    continue
                case 37 | 40 | 41 | 42:
                    carregar_depois = operacoes[i.num_gramatica]
                    continue
                case 21 | 38 | 35 | 29:
                    if carregar_depois:
                        final.append(carregar_depois)
                        carregar_depois = None      
                case 30:
                    carregar_depois = "INVE"
                    continue
                case 20:
                    final.append("LEIT")    
                case _:
                    continue
    destino, instrucoes, chaves = {}, [], []
    for i in final:
        if i.endswith(":"):
            destino[i[:-1]] = len(instrucoes)+1
            chaves.append(i[:-1])
        else:
            instrucoes.append(i)
    for j in range(len(instrucoes)):
        if any(termo in instrucoes[j] for termo in ["DSVI", "DSVF"]):
            indice = instrucoes[j].split(" ")[-1]
            pos = str(destino[indice])
            valor = instrucoes[j].replace(instrucoes[j].split(" ")[-1], pos)
            instrucoes.pop(j)
            instrucoes.insert(j, valor)
    final = instrucoes
    final.append("PARA")
    return final

def analisador_sintatico(tokens):
    pilha_estado = [0]
    reducao = []
    simbolos = []
    tabela_simbolos = []
    linhas = []
    entrada = tokens
    entrada.append(("FIMDECADEIA", "&"))
    entrada_atual = entrada[0][0]
    try:
        while entrada:
            pos = pilha_estado[-1]
            acao, pos = ESTADOS[pos][entrada_atual]

            if len(simbolos) > 0 and simbolos[-1][0] == "ID":
                if not simbolos[-1][1] in tabela_simbolos:
                    simb = Simbolo(simbolos[-1][1], None)
                    tabela_simbolos.append(simb)
            if acao == Status.SUCESSO:
                return gerar_codigo(reducao)
            if acao == Status.SHIFT:
                simbolos.append(entrada.pop(0))
                pilha_estado.append(pos)
                entrada_atual = entrada[0][0]
            elif acao == Status.REDUZ:
                vars = []
                palavra, qtd_subs = GRAMATICA[pos]
                for i in range(qtd_subs):
                    vars.append(simbolos[-1])
                    simbolos.pop()
                    pilha_estado.pop()
                reducao.append(ReducaoGramatica(pos, vars, len(reducao)))
                simbolos.append(palavra)
                entrada_atual = palavra
            elif acao == Status.DESVIO:
                pilha_estado.append(pos)
                entrada_atual = entrada[0][0]
    except KeyError:
        print("ERRO! Símbolo inesperado na entrada.")
        return False
    return False

ESTADOS = {
    0: {"ABREPHP": (Status.SHIFT, 1)},
    1: {
        "FECHAPHP": (Status.REDUZ, 10),
        "PONTOVIRG": (Status.REDUZ, 10),
        "ID": (Status.SHIFT, 5),
        "IF": (Status.SHIFT, 3),
        "WHILE": (Status.SHIFT, 7),
        "ECHO": (Status.SHIFT, 4),
        "DC": (Status.DESVIO, 16),
        "VAR": (Status.DESVIO, 79),
        "VARS":(Status.DESVIO, 80),
        "CMDS": (Status.DESVIO, 17),
        "CMD_COND": (Status.DESVIO, 6),
        "CMD": (Status.DESVIO, 2)
        },
    2: {
        "PONTOVIRG": (Status.SHIFT, 9),
        "MAIS_CMDS": (Status.DESVIO, 21)
    },
    3: {
        "ABRE_PAR": (Status.SHIFT, 10)
    },
    4: {
        "ID": (Status.SHIFT, 8)
    },
    5: {
        "VIRGULA": (Status.SHIFT, 14),
        "PONTOVIRG": (Status.REDUZ, 6),
        "ATRIB": (Status.SHIFT, 13),
        "MAIS_VAR": (Status.DESVIO, 15),
        "RESTO_IDENT": (Status.DESVIO, 12)
    },
    6: {
        "IF": (Status.SHIFT, 3),
        "WHILE": (Status.SHIFT, 7),
        "ECHO": (Status.SHIFT, 4),
        "ID": (Status.SHIFT, 5),
        "VAR": (Status.DESVIO, 79),
        "VARS":(Status.DESVIO, 80),
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10),
        "DC": (Status.DESVIO, 16), 
        "CMDS": (Status.DESVIO, 56),
        "CMD_COND": (Status.DESVIO, 6),
        "CMD": (Status.DESVIO, 2)
    },
    7: {
        "ABRE_PAR": (Status.SHIFT, 11)
    },
    8: {
        "PONTO": (Status.SHIFT, 19)
    },
    9: {
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10),
        "DC": (Status.DESVIO, 16),
        "CMDS": (Status.DESVIO, 22),
        "CMD_COND": (Status.DESVIO, 6),
        "ID": (Status.SHIFT, 5),
        "IF": (Status.SHIFT, 3),
        "WHILE": (Status.SHIFT, 7),
        "ECHO": (Status.SHIFT, 4),
        "VAR": (Status.DESVIO, 79),
        "VARS":(Status.DESVIO, 80),
        "CMD":(Status.DESVIO, 2)
    },
    10: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "MENOS": (Status.SHIFT, 50),
        "NUM_REAL": (Status.REDUZ, 31),
        "CONDICAO": (Status.DESVIO, 23),
        "EXPRESSAO": (Status.DESVIO, 57),
        "TERMO": (Status.DESVIO, 38),
        "OP_UN": (Status.DESVIO, 41)
    },
    11: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "MENOS": (Status.SHIFT, 50),
        "NUM_REAL": (Status.REDUZ, 31),
        "CONDICAO": (Status.DESVIO, 24),
        "EXPRESSAO": (Status.DESVIO, 57),
        "TERMO": (Status.DESVIO, 38),
        "OP_UN": (Status.DESVIO, 41)
    },
    12: {
        "PONTOVIRG": (Status.REDUZ, 15)
    },
    13: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "FLOATVAL": (Status.SHIFT, 61),
        "MENOS": (Status.SHIFT, 50),
        "NUM_REAL": (Status.REDUZ, 31),
        "EXP_IDENT": (Status.DESVIO, 37),
        "EXPRESSAO": (Status.DESVIO, 60),
        "TERMO": (Status.DESVIO, 38),
        "OP_UN": (Status.DESVIO, 41)
    },
    14: {
        "ID": (Status.SHIFT, 36)
    },
    15: {
        "PONTOVIRG": (Status.REDUZ, 4)
    },
    16: {
        "FECHAPHP": (Status.REDUZ, 9),
        "FECHA_CHAVE": (Status.REDUZ, 9)
    },
    17: {
        "FECHAPHP": (Status.SHIFT, 18)
    },
    18: {
        "FIMDECADEIA": (Status.SUCESSO, "OK")
    },
    19: {
        "PHP_EOL": (Status.SHIFT, 20)
    },
    20: {
        "PONTOVIRG": (Status.REDUZ, 14)
    },
    21:{
        "FECHAPHP": (Status.REDUZ, 7),
        "FECHA_CHAVE": (Status.REDUZ, 7)
    },
    22: {
        "FECHAPHP": (Status.REDUZ, 11),
        "FECHA_CHAVE": (Status.REDUZ, 11)
    },
    23: {
        "FECHA_PAR": (Status.SHIFT, 25)
    },
    24: {
        "FECHA_PAR": (Status.SHIFT, 26)
    },
    25: {
        "ABRE_CHAVE": (Status.SHIFT, 28)
    },
    26: {
        "ABRE_CHAVE": (Status.SHIFT, 27)
    },
    27: {
        "FECHAPHP": (Status.REDUZ, 10),
        "IF": (Status.SHIFT, 3),
        "FECHA_CHAVE": (Status.REDUZ, 10),
        "DC": (Status.DESVIO, 16),
        "CMDS": (Status.DESVIO, 32),
        "CMD_COND": (Status.DESVIO, 6),
        "CMD": (Status.DESVIO, 2),
        "ID": (Status.SHIFT, 5),
        "WHILE": (Status.SHIFT, 7),
        "ECHO": (Status.SHIFT, 4),
        "VAR": (Status.DESVIO, 79),
        "VARS":(Status.DESVIO, 80)
    },
    28: {
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10),
        "DC": (Status.DESVIO, 16),
        "IF": (Status.SHIFT, 3),
        "CMDS": (Status.DESVIO, 29),
        "CMD_COND": (Status.DESVIO, 6),
        "CMD": (Status.DESVIO, 2),
        "ID": (Status.SHIFT, 5),
        "WHILE": (Status.SHIFT, 7),
        "ECHO": (Status.SHIFT, 4),
        "VAR": (Status.DESVIO, 79),
        "VARS":(Status.DESVIO, 80)
    },
    29: {
        "FECHA_CHAVE": (Status.SHIFT, 30)
    },
    30: {
        "FECHAPHP": (Status.REDUZ, 17),
        "ID": (Status.REDUZ, 17),
        "IF": (Status.REDUZ, 17),
        "FECHA_CHAVE": (Status.REDUZ, 17),
        "WHILE": (Status.REDUZ, 17),
        "ECHO": (Status.REDUZ, 17),
        "ELSE": (Status.SHIFT, 34),
        "PFALSA": (Status.DESVIO, 31)
    },
    31: {
        "FECHAPHP": (Status.REDUZ, 12),
        "ID": (Status.REDUZ, 12),
        "IF": (Status.REDUZ, 12),
        "FECHA_CHAVE": (Status.REDUZ, 12),
        "WHILE": (Status.REDUZ, 12),
        "ECHO": (Status.REDUZ, 12)
    },
    32: {
        "FECHA_CHAVE": (Status.SHIFT, 33)
    },
    33: {
        "FECHAPHP": (Status.REDUZ, 13),
        "FECHA_CHAVE": (Status.REDUZ, 13),
        "ID": (Status.REDUZ, 13),
        "IF": (Status.REDUZ, 13),
        "WHILE": (Status.REDUZ, 13),
        "ECHO": (Status.REDUZ, 13)
    },
    34: {
        "ABRE_CHAVE": (Status.SHIFT, 35)
    },
    35: {
        "ID": (Status.SHIFT, 5),
        "IF": (Status.SHIFT, 3),
        "WHILE": (Status.SHIFT, 7),
        "ECHO": (Status.SHIFT, 4),
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10),
        "DC": (Status.DESVIO, 16),
        "CMDS": (Status.DESVIO, 67),
        "CMD_COND": (Status.DESVIO, 6),
        "CMD": (Status.DESVIO, 2),
        "VAR": (Status.DESVIO, 79),
        "VARS": (Status.DESVIO, 80)
    },
    36: {
        "VIRGULA": (Status.SHIFT, 14),
        "PONTOVIRG": (Status.REDUZ, 6),
        "MAIS_VAR": (Status.DESVIO, 82)
    },
    37: {
        "PONTOVIRG": (Status.REDUZ, 18)
    },
    38: {
        "PONTOVIRG": (Status.REDUZ, 36),
        "FECHA_PAR": (Status.REDUZ, 36),
        "IGUAL_IGUAL": (Status.REDUZ, 36),
        "DIFERENTE": (Status.REDUZ, 36),
        "MAIOR_IGUAL": (Status.REDUZ, 36),
        "MENOR_IGUAL": (Status.REDUZ, 36),
        "MENOR": (Status.REDUZ, 36),
        "MAIOR": (Status.REDUZ, 36),
        "MENOS": (Status.SHIFT, 46),
        "MAIS": (Status.SHIFT, 45),
        "OUTROS_TERMOS": (Status.DESVIO, 39),
        "OP_AD": (Status.DESVIO, 40)
    },
    39: {
        "PONTOVIRG": (Status.REDUZ, 28),
        "FECHA_PAR": (Status.REDUZ, 28),
        "IF": (Status.REDUZ, 28),
        "IGUAL_IGUAL": (Status.REDUZ, 28),
        "DIFERENTE": (Status.REDUZ, 28),
        "MAIOR_IGUAL": (Status.REDUZ, 28),
        "MENOR_IGUAL": (Status.REDUZ, 28),
        "MENOR": (Status.REDUZ, 28),
        "MAIOR": (Status.REDUZ, 28)
    },
    40: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "NUM_REAL": (Status.REDUZ, 31),
        "MENOS": (Status.SHIFT, 50),
        "TERMO": (Status.DESVIO, 42),
        "OP_UN": (Status.DESVIO, 41)
    },
    41: {
        "ID": (Status.SHIFT, 47),
        "ABRE_PAR": (Status.SHIFT, 49),
        "NUM_REAL": (Status.SHIFT, 48),
        "FATOR": (Status.DESVIO, 43)
    },
    42: {
        "PONTOVIRG": (Status.REDUZ, 36),
        "FECHA_PAR": (Status.REDUZ, 36),
        "IGUAL_IGUAL": (Status.REDUZ, 36),
        "DIFERENTE": (Status.REDUZ, 36),
        "MAIOR_IGUAL": (Status.REDUZ, 36),
        "MENOR_IGUAL": (Status.REDUZ, 36),
        "MENOR": (Status.REDUZ, 36),
        "MAIOR": (Status.REDUZ, 36),
        "MENOS": (Status.SHIFT, 46),
        "MAIS": (Status.SHIFT, 45),
        "OUTROS_TERMOS": (Status.DESVIO, 44),
        "OP_AD": (Status.DESVIO, 40)
    },
    43: {
        "PONTOVIRG": (Status.REDUZ, 39),
        "FECHA_PAR": (Status.REDUZ, 39),
        "IGUAL_IGUAL": (Status.REDUZ, 39),
        "DIFERENTE": (Status.REDUZ, 39),
        "MAIOR_IGUAL": (Status.REDUZ, 39),
        "MENOR_IGUAL": (Status.REDUZ, 39),
        "MENOR": (Status.REDUZ, 39),
        "MAIOR": (Status.REDUZ, 39),
        "MENOS": (Status.REDUZ, 39),
        "MAIS": (Status.REDUZ, 39),
        "MULT": (Status.SHIFT, 53),
        "DIV": (Status.SHIFT, 54),
        "MAIS_FATORES": (Status.DESVIO, 69),
        "OP_MUL": (Status.DESVIO, 70)
    },
    44: {
        "PONTOVIRG": (Status.REDUZ, 35),
        "FECHA_PAR": (Status.REDUZ, 35),
        "IGUAL_IGUAL": (Status.REDUZ, 35),
        "DIFERENTE": (Status.REDUZ, 35),
        "MAIOR_IGUAL": (Status.REDUZ, 35),
        "MENOR_IGUAL": (Status.REDUZ, 35),
        "MENOR": (Status.REDUZ, 35),
        "MAIOR": (Status.REDUZ, 35)
    },
    45: {
        "ID": (Status.REDUZ, 37),
        "ABRE_PAR": (Status.REDUZ, 37),
        "MENOS": (Status.REDUZ, 37),
        "NUM_REAL": (Status.REDUZ, 37)
    },
    46: {
        "ID": (Status.REDUZ, 42),
        "ABRE_PAR": (Status.REDUZ, 42),
        "MENOS": (Status.REDUZ, 42),
        "NUM_REAL": (Status.REDUZ, 42)
    },
    47: {
        "PONTOVIRG": (Status.REDUZ, 32),
        "FECHA_PAR": (Status.REDUZ, 32),
        "IGUAL_IGUAL": (Status.REDUZ, 32),
        "DIFERENTE": (Status.REDUZ, 32),
        "MAIOR_IGUAL": (Status.REDUZ, 32),
        "MENOR_IGUAL": (Status.REDUZ, 32),
        "MENOR": (Status.REDUZ, 32),
        "MAIOR": (Status.REDUZ, 32),
        "MENOS": (Status.REDUZ, 32),
        "MAIS": (Status.REDUZ, 32),
        "MULT": (Status.REDUZ, 32),
        "DIV": (Status.REDUZ, 32)
    },
    48: {
        "PONTOVIRG": (Status.REDUZ, 33),
        "FECHA_PAR": (Status.REDUZ, 33),
        "IGUAL_IGUAL": (Status.REDUZ, 33),
        "DIFERENTE": (Status.REDUZ, 33),
        "MAIOR_IGUAL": (Status.REDUZ, 33),
        "MENOR_IGUAL": (Status.REDUZ, 33),
        "MENOR": (Status.REDUZ, 33),
        "MAIOR": (Status.REDUZ, 33),
        "MENOS": (Status.REDUZ, 33),
        "MAIS": (Status.REDUZ, 33),
        "MULT": (Status.REDUZ, 33),
        "DIV": (Status.REDUZ, 33)
    },
    49: {
        "ID": (Status.REDUZ, 30),
        "FECHA_PAR": (Status.REDUZ, 30),
        "NUM_REAL": (Status.REDUZ, 30),
        "MENOS": (Status.SHIFT, 50),
        "EXPRESSAO": (Status.DESVIO, 51),
        "TERMO": (Status.DESVIO, 38),
        "OP_UN": (Status.DESVIO, 41)
    },
    50: {
        "ID": (Status.REDUZ, 30),
        "FECHA_PAR": (Status.REDUZ, 30),
        "NUM_REAL": (Status.REDUZ, 30)
    },
    51: {
        "FECHA_PAR": (Status.SHIFT, 52)
    },
    52: {
        "PONTOVIRG": (Status.REDUZ, 34),
        "FECHA_PAR": (Status.REDUZ, 34),
        "IGUAL_IGUAL": (Status.REDUZ, 34),
        "DIFERENTE": (Status.REDUZ, 34),
        "MAIOR_IGUAL": (Status.REDUZ, 34),
        "MENOR_IGUAL": (Status.REDUZ, 34),
        "MENOR": (Status.REDUZ, 34),
        "MAIOR": (Status.REDUZ, 34),
        "MENOS": (Status.REDUZ, 34),
        "MAIS": (Status.REDUZ, 34),
        "MULT": (Status.REDUZ, 34),
        "DIV": (Status.REDUZ, 34)
    },
    53: {
        "ID": (Status.REDUZ, 40),
        "FECHA_PAR": (Status.REDUZ, 40),
        "NUM_REAL": (Status.REDUZ, 40)
    },
    54: {
        "ID": (Status.REDUZ, 41),
        "FECHA_PAR": (Status.REDUZ, 41),
        "NUM_REAL": (Status.REDUZ, 41)
    },
    56: {
      "FECHAPHP": (Status.REDUZ, 8),  
      "FECHA_CHAVE": (Status.REDUZ, 8)
    },
    57: {
        "IGUAL_IGUAL": (Status.SHIFT, 73),
        "DIFERENTE": (Status.SHIFT, 74),
        "MAIOR_IGUAL": (Status.SHIFT, 75),
        "MENOR_IGUAL": (Status.SHIFT, 76),
        "MENOR": (Status.SHIFT, 78),
        "MAIOR": (Status.SHIFT, 77),
        "RELACAO": (Status.DESVIO, 58)
    },
    58: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "NUM_REAL": (Status.REDUZ, 31),
        "MENOS": (Status.SHIFT, 50),
        "EXPRESSAO": (Status.DESVIO, 59),
        "TERMO": (Status.DESVIO, 38),
        "OP_UN": (Status.DESVIO, 41)
    },
    59: {
        "FECHA_PAR": (Status.REDUZ, 21)
    },
    60: {
        "PONTOVIRG": (Status.REDUZ, 19)
    },
    61: {
        "ABRE_PAR": (Status.SHIFT, 62)    
    },
    62: {
        "READLINE": (Status.SHIFT, 63)
    },
    63: {
        "ABRE_PAR": (Status.SHIFT, 64)
    },
    64: {
        "FECHA_PAR": (Status.SHIFT, 65)
    },
    65: {
        "FECHA_PAR": (Status.SHIFT, 66)
    },
    66: {
        "PONTOVIRG": (Status.REDUZ, 20)
    },
    67: {
        "FECHA_CHAVE": (Status.SHIFT, 68)
    },
    68: {
        "FECHAPHP": (Status.REDUZ, 16),
        "FECHA_CHAVE": (Status.REDUZ, 16),
        "ID": (Status.REDUZ, 16),
        "IF": (Status.REDUZ, 16),
        "WHILE": (Status.REDUZ, 16), 
        "ECHO": (Status.REDUZ, 16)
    },
    69: {
        "PONTOVIRG": (Status.REDUZ, 29),
        "FECHA_PAR": (Status.REDUZ, 29),
        "IGUAL_IGUAL": (Status.REDUZ, 29),
        "DIFERENTE": (Status.REDUZ, 29),
        "MAIOR_IGUAL": (Status.REDUZ, 29),
        "MENOR_IGUAL": (Status.REDUZ, 29),
        "MENOR": (Status.REDUZ, 29),
        "MAIOR": (Status.REDUZ, 29),
        "MENOS": (Status.REDUZ, 29),
        "MAIS": (Status.REDUZ, 29)
    },
    70: {
        "ID": (Status.SHIFT, 47),
        "ABRE_PAR": (Status.SHIFT, 49),
        "NUM_REAL": (Status.SHIFT, 48),
        "FATOR": (Status.DESVIO, 71)
    },
    71: {
        "PONTOVIRG": (Status.REDUZ, 39),
        "FECHA_PAR": (Status.REDUZ, 39),
        "IGUAL_IGUAL": (Status.REDUZ, 39),
        "DIFERENTE": (Status.REDUZ, 39),
        "MAIOR_IGUAL": (Status.REDUZ, 39),
        "MENOR_IGUAL": (Status.REDUZ, 39),
        "MENOR": (Status.REDUZ, 39),
        "MAIOR": (Status.REDUZ, 39),
        "MENOS": (Status.REDUZ, 39),
        "MAIS":  (Status.REDUZ, 39),
        "MULT": (Status.SHIFT, 53),
        "DIV": (Status.SHIFT, 54),
        "MAIS_FATORES": (Status.DESVIO, 72),
        "OP_MUL": (Status.DESVIO, 70)
    },
    72: {
        "PONTOVIRG": (Status.REDUZ, 38),
        "FECHA_PAR": (Status.REDUZ, 38),
        "IGUAL_IGUAL": (Status.REDUZ, 38),
        "DIFERENTE": (Status.REDUZ, 38),
        "MAIOR_IGUAL": (Status.REDUZ, 38),
        "MENOR_IGUAL": (Status.REDUZ, 38),
        "MENOR": (Status.REDUZ, 38),
        "MAIOR": (Status.REDUZ, 38),
        "MENOS": (Status.REDUZ, 38),
        "MAIS":  (Status.REDUZ, 38),
    },
    73: {
        "ID": (Status.REDUZ, 22),
        "ABRE_PAR": (Status.REDUZ, 22),
        "MENOS": (Status.REDUZ, 22),
        "NUM_REAL": (Status.REDUZ, 22)
    },
    74: {
        "ID": (Status.REDUZ, 23),
        "ABRE_PAR": (Status.REDUZ, 23),
        "MENOS": (Status.REDUZ, 23),
        "NUM_REAL": (Status.REDUZ, 23)
    },
    75: {
        "ID": (Status.REDUZ, 24),
        "ABRE_PAR": (Status.REDUZ, 24),
        "MENOS": (Status.REDUZ, 24),
        "NUM_REAL": (Status.REDUZ, 24)
    },
    76: {
        "ID": (Status.REDUZ, 25),
        "ABRE_PAR": (Status.REDUZ, 25),
        "MENOS": (Status.REDUZ, 25),
        "NUM_REAL": (Status.REDUZ, 25)
    },
    77: {
        "ID": (Status.REDUZ, 26),
        "ABRE_PAR": (Status.REDUZ, 26),
        "MENOS": (Status.REDUZ, 26),
        "NUM_REAL": (Status.REDUZ, 26)
    },
    78: {
        "ID": (Status.REDUZ, 27),
        "ABRE_PAR": (Status.REDUZ, 27),
        "MENOS": (Status.REDUZ, 27),
        "NUM_REAL": (Status.REDUZ, 27)
    },
    79: {
        "PONTOVIRG": (Status.SHIFT, 9),
        "MAIS_CMDS": (Status.DESVIO, 81)
    },
    80: {
        "PONTOVIRG": (Status.REDUZ, 3)
    },
    81: {
        "FECHAPHP": (Status.REDUZ, 2),
        "FECHA_CHAVE": (Status.REDUZ, 2)
    },
    82: {
        "PONTOVIRG": (Status.REDUZ, 5)
    }
}

GRAMATICA = {
    1: ("PROG", 3),
    2: ("DC", 2),
    3: ("VAR", 1),
    4: ("VARS", 2),
    5: ("MAIS_VAR", 3),
    6: ("MAIS_VAR", 0),
    7: ("CMDS", 2),
    8: ("CMDS", 2),
    9: ("CMDS", 1),
    10: ("CMDS", 0),
    11: ("MAIS_CMDS", 2),
    12: ("CMD_COND", 8),
    13: ("CMD_COND", 7),
    14: ("CMD", 4),
    15: ("CMD", 2),
    16: ("PFALSA", 4),
    17: ("PFALSA", 0),
    18: ("RESTO_IDENT", 2),
    19: ("EXP_IDENT", 1),
    20: ("EXP_IDENT", 6),
    21: ("CONDICAO", 3),
    22: ("RELACAO", 1),
    23: ("RELACAO", 1),
    24: ("RELACAO", 1),
    25: ("RELACAO", 1),
    26: ("RELACAO", 1),
    27: ("RELACAO", 1),
    28: ("EXPRESSAO", 2),
    29: ("TERMO", 3),
    30: ("OP_UN", 1),
    31: ("OP_UN", 0),
    32: ("FATOR", 1),
    33: ("FATOR", 1),
    34: ("FATOR", 3),
    35: ("OUTROS_TERMOS", 3),
    36: ("OUTROS_TERMOS", 0),
    37: ("OP_AD", 1),
    38: ("MAIS_FATORES", 3),
    39: ("MAIS_FATORES", 0),
    40: ("OP_MUL", 1),
    41: ("OP_MUL", 1),
    42: ("OP_AD", 1)
}