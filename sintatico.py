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

def gerar_codigo(lista_gramatica):
    REL = {22: "CPIG", 23: "CDES", 24: "CMAI", 25: "CPMI", 26: "CPMA", 27: "CPME"}
    tabela = {}        # variável -> endereço
    rotulos = [0]
    pilha = []         # um fragmento por não-terminal ainda sem "pai"

    def novo_rotulo():
        rotulos[0] += 1
        return f"L{rotulos[0]}"

    def endereco(nome):
        if nome not in tabela:
            raise ValueError(f"Variável '{nome}' usada sem declaração.")
        return tabela[nome]

    try:
        for r in lista_gramatica:
            a = []
            for f in r.filhos:
                a.append(f[1] if isinstance(f, tuple) else pilha.pop())
            a.reverse()                  
            print(f"--------{r.num_gramatica}--------")
            print(f"a: {a}")
            print(f"Pilha Antes: {pilha}")
            match r.num_gramatica:
                case 2:  cod = a[1]                          # DC -> VAR MAIS_CMDS
                case 3:                                      # VAR -> VARS
                    for nome in a[0]:
                        if nome in tabela:
                            raise ValueError(f"Variável '{nome}' declarada mais de uma vez.")
                        tabela[nome] = len(tabela)
                    cod = []
                case 4:  cod = [a[0]] + a[1]                 # VARS -> ID MAIS_VAR
                case 5:  cod = [a[1]] + a[2]                 # MAIS_VAR -> , ID MAIS_VAR
                case 6:  cod = []                            # MAIS_VAR -> ε

                # ---------- comandos ----------
                case 7 | 8:  cod = a[0] + a[1]               # CMDS -> CMD MAIS_CMDS | CMD_COND CMDS
                case 9:      cod = a[0]                      # CMDS -> DC
                case 10:     cod = []                        # CMDS -> ε
                case 11:     cod = a[1]                      # MAIS_CMDS -> ; CMDS

                case 12:                                     # IF ( COND ) { CMDS } PFALSA
                    cond, corpo, falsa = a[2], a[5], a[7]
                    if falsa is None:
                        l_fim = novo_rotulo()
                        cod = cond + [f"DSVF {l_fim}"] + corpo + [f"{l_fim}:"]
                    else:
                        l_else, l_fim = novo_rotulo(), novo_rotulo()
                        cod = (cond + [f"DSVF {l_else}"] + corpo + [f"DSVI {l_fim}", f"{l_else}:"]
                               + falsa + [f"{l_fim}:"])
                case 13:                                     # WHILE ( COND ) { CMDS }
                    l_ini, l_fim = novo_rotulo(), novo_rotulo()
                    cod = ([f"{l_ini}:"] + a[2] + [f"DSVF {l_fim}"] + a[5]
                           + [f"DSVI {l_ini}", f"{l_fim}:"])

                case 14: cod = [f"CRVL {endereco(a[1])}", "IMPR"]    # ECHO ID . PHP_EOL
                case 15: cod = a[1] + [f"ARMZ {endereco(a[0])}"]     # ID RESTO_IDENT
                case 16: cod = a[2]                                  # PFALSA -> ELSE { CMDS }
                case 17: cod = None                                  # PFALSA -> ε (sem else)

                case 18: cod = a[1]                          # RESTO_IDENT -> = EXP_IDENT
                case 19: cod = a[0]                          # EXP_IDENT -> EXPRESSAO
                case 20: cod = ["LEIT"]                      # EXP_IDENT -> floatval(readline())

                # ---------- condição e expressões ----------
                case 21: cod = a[0] + a[2] + a[1]            # EXPR RELACAO EXPR
                case 22 | 23 | 24 | 25 | 26 | 27: cod = [REL[r.num_gramatica]]

                case 28: cod = a[0] + a[1]                   # EXPRESSAO -> TERMO OUTROS_TERMOS
                case 29: cod = a[1] + a[0] + a[2]            # TERMO -> OP_UN FATOR MAIS_FATORES
                case 30: cod = ["INVE"]                      # OP_UN -> -
                case 31: cod = []                            # OP_UN -> ε

                case 32: cod = [f"CRVL {endereco(a[0])}"]    # FATOR -> ID
                case 33: cod = [f"CRCT {a[0]}"]              # FATOR -> NUM_REAL
                case 34: cod = a[1]                          # FATOR -> ( EXPRESSAO )

                # operando, depois operador, depois o resto => associatividade à esquerda
                case 35 | 38: cod = a[1] + a[0] + a[2]
                case 36 | 39: cod = []

                case 37: cod = ["SOMA"]
                case 42: cod = ["SUBT"]
                case 40: cod = ["MULT"]
                case 41: cod = ["DIVI"]

                case _:
                    raise ValueError(f"Produção {r.num_gramatica} sem tradução.")

            pilha.append(cod)
            print(f"Pilha Depois: {pilha}")
    except ValueError as e:
        print(f"ERRO SEMÂNTICO: {e}")
        return None

    # PROG -> ABREPHP CMDS FECHAPHP (ABREPHP/FECHAPHP são terminais: nunca são reduzidos)
    codigo = ["INPP"]
    if tabela:
        codigo.append(f"ALME {len(tabela)}")      # um único ALME com o total
    codigo += pilha[-1] + ["PARA"]

    # troca rótulos (L1:, DSVF L1) por endereços
    destino, instrucoes = {}, []
    for ins in codigo:
        if ins.endswith(":"):
            destino[ins[:-1]] = len(instrucoes)   # use +1 se sua máquina conta do 1
        else:
            instrucoes.append(ins)
    final = []
    for ins in instrucoes:
        op, *arg = ins.split()
        if op in ("DSVI", "DSVF"):
            ins = f"{op} {destino[arg[0]]}"
        final.append(ins)
    return final

def analisador_sintatico(tokens):
    pilha_estado = [0]
    reducao = []
    simbolos = []
    tabela_simbolos = []
    linhas = []
    entrada = tokens
    entrada.append(("FIMDECADEIA", "&")) # fim de cadeia :D
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
                print("SUCESSO!")
                print("-----------------------------")
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
        print(simbolos)
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