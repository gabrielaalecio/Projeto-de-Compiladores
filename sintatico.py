from enum import Enum

class Status(Enum):
    SHIFT = "S"
    REDUZ = "R"

ACTION = {
    0: {"ABREPHP": (Status.SHIFT, 1)},
    1: {
        "FECHAPHP": (Status.REDUZ, 10),
        "PONTOVIRG": (Status.REDUZ, 10),
        "ID": (Status.SHIFT, 5),
        "IF": (Status.SHIFT, 3),
        "WHILE": (Status.SHIFT, 7),
        "ECHO": (Status.SHIFT, 4)
        },
    2: {
        "PONTOVIRG": (Status.SHIFT, 9)
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
        "ATRIB": (Status.SHIFT, 13)
    },
    6: {
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10)
    },
    7: {
        "ABRE_PAR": (Status.SHIFT, 11)
    },
    8: {
        "PONTO": (Status.SHIFT, 19)
    },
    9: {
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10)
    },
    10: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "MENOS": (Status.SHIFT, 50),
        "NUM_REAL": (Status.REDUZ, 31)
    },
    11: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "MENOS": (Status.SHIFT, 50),
        "NUM_REAL": (Status.REDUZ, 31)
    },
    12: {
        "PONTOVIRG": (Status.REDUZ, 15)
    },
    13: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "FLOATVAL": (Status.SHIFT, 61),
        "MENOS": (Status.SHIFT, 50),
        "NUM_REAL": (Status.REDUZ, 31)
    },
    14: {
        "ID": (Status.REDUZ, 36)
    },
    15: {
        "PONTOVIRG": (Status.REDUZ, 4)
    },
    16: {
        "FECHAPHP": (Status.REDUZ, 9),
        "FECHA_CHAVE": (Status.REDUZ, 9)
    },
    17: {
        "ABREPHP": (Status.SHIFT, 18)
    },
    18: {
        "FIMDECADEIA": "SUCESSO"
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
        "FECHA_CHAVE": (Status.SHIFT, 28)
    },
    26: {
        "ABRE_CHAVE": (Status.SHIFT, 27)
    },
    27: {
        "FECHAPHP": (Status.REDUZ, 10),
        "IF": (Status.SHIFT, 3),
        "FECHA_CHAVE": (Status.REDUZ, 10),
        "WHILE": (Status.REDUZ, 10)
    },
    28: {
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10)
    },
    29: {
        "FECHA_CHAVE": (Status.SHIFT, 30)
    },
    30: {
        "FECHAPHP": (Status.REDUZ, 12),
        "ID": (Status.REDUZ, 12),
        "IF": (Status.REDUZ, 12),
        "FECHA_CHAVE": (Status.REDUZ, 12),
        "WHILE": (Status.REDUZ, 12),
        "ECHO": (Status.REDUZ, 12),
        "ELSE": (Status.SHIFT, 34)
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
        "ID": (Status.REDUZ, 13),
        "IF": (Status.REDUZ, 13),
        "WHILE": (Status.REDUZ, 13),
        "ECHO": (Status.REDUZ, 13)
    },
    34: {
        "FECHA_CHAVE": (Status.SHIFT, 35)
    },
    35: {
        "FECHAPHP": (Status.REDUZ, 10),
        "FECHA_CHAVE": (Status.REDUZ, 10)
    },
    36: {
        "VIRGULA": (Status.SHIFT, 14)
    },
    37: {
        "PONTOVIRG": (Status.REDUZ, 18)
    },
    38: {
        "IF": (Status.REDUZ, 36),
        "IGUAL_IGUAL": (Status.REDUZ, 36),
        "DIFERENTE": (Status.REDUZ, 36),
        "MAIOR_IGUAL": (Status.REDUZ, 36),
        "MENOR_IGUAL": (Status.REDUZ, 36),
        "MENOR": (Status.REDUZ, 36),
        "MAIOR": (Status.REDUZ, 36),
        "MENOS": (Status.SHIFT, 46),
        "MAIS": (Status.SHIFT, 45)
    },
    39: {
        "IF": (Status.REDUZ, 28),
        "IGUAL_IGUAL": (Status.REDUZ, 28),
        "DIFERENTE": (Status.REDUZ, 28),
        "MAIOR_IGUAL": (Status.REDUZ, 28),
        "MENOR_IGUAL": (Status.REDUZ, 28),
        "MENOR": (Status.REDUZ, 28),
        "MAIOR": (Status.REDUZ, 28)
    },
    40: {
        "ID": (Status.REDUZ, 21),
        "ABRE_PAR": (Status.REDUZ, 21),
        "NUM_REAL": (Status.REDUZ, 21),
        "MENOS": (Status.SHIFT, 50)
    },
    41: {
        "ID": (Status.SHIFT, 47),
        "FECHA_PAR": (Status.SHIFT, 43),
        "NUM_REAL": (Status.SHIFT, 48)
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
        "MAIS": (Status.SHIFT, 45)
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
        "DIV": (Status.SHIFT, 54)
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
        "MULT": (Status.REDUZ, 32),
        "DIV": (Status.REDUZ, 33)
    },
    49: {
        "ID": (Status.REDUZ, 30),
        "FECHA_PAR": (Status.REDUZ, 30),
        "NUM_REAL": (Status.REDUZ, 30),
        "MENOS": (Status.SHIFT, 50)
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
      "WHILE": (Status.REDUZ, 8)
    },
    57: {
        "IGUAL_IGUAL": (Status.SHIFT, 73),
        "DIFERENTE": (Status.SHIFT, 74),
        "MAIOR_IGUAL": (Status.SHIFT, 75),
        "MENOR_IGUAL": (Status.SHIFT, 76),
        "MENOR": (Status.SHIFT, 78),
        "MAIOR": (Status.SHIFT, 77)
    },
    58: {
        "ID": (Status.REDUZ, 31),
        "ABRE_PAR": (Status.REDUZ, 31),
        "NUM_REAL": (Status.REDUZ, 31),
        "MENOS": (Status.SHIFT, 50)
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
        "FECHA_CHAVE": (Status.SHIFT, 66)
    },
    66: {
        "PONTOVIRG": (Status.REDUZ, 20)
    },
    67: {
        "FECHA_CHAVE": (Status.SHIFT, 68)
    },
    68: {
        "FECHAPHP": (Status.REDUZ, 16),
        "ID": (Status.REDUZ, 16),
        "IF": (Status.REDUZ, 16),
        "FECHA_PAR": (Status.REDUZ, 16), 
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
        "MAIOR": (Status.REDUZ, 29)
    },
    70: {
        "ID": (Status.SHIFT, 47),
        "ABRE_PAR": (Status.SHIFT, 49),
        "NUM_REAL": (Status.SHIFT, 48)
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
        "MULT": (Status.SHIFT, 53),
        "DIV": (Status.SHIFT, 54)
    },
    72: {
        "PONTOVIRG": (Status.REDUZ, 38),
        "FECHA_PAR": (Status.REDUZ, 38),
        "IGUAL_IGUAL": (Status.REDUZ, 38),
        "DIFERENTE": (Status.REDUZ, 38),
        "MAIOR_IGUAL": (Status.REDUZ, 38),
        "MENOR_IGUAL": (Status.REDUZ, 38),
        "MENOR": (Status.REDUZ, 38),
        "MAIOR": (Status.REDUZ, 38)
    },
    73: {
        "ID": (Status.REDUZ, 22),
        "FECHA_PAR": (Status.REDUZ, 22),
        "MENOS": (Status.REDUZ, 22),
        "NUM_REAL": (Status.REDUZ, 22)
    },
    74: {
        "ID": (Status.REDUZ, 23),
        "FECHA_PAR": (Status.REDUZ, 23),
        "MENOS": (Status.REDUZ, 23),
        "NUM_REAL": (Status.REDUZ, 23)
    },
    75: {
        "ID": (Status.REDUZ, 24),
        "FECHA_PAR": (Status.REDUZ, 24),
        "MENOS": (Status.REDUZ, 24),
        "NUM_REAL": (Status.REDUZ, 24)
    },
    76: {
        "ID": (Status.REDUZ, 25),
        "FECHA_PAR": (Status.REDUZ, 25),
        "MENOS": (Status.REDUZ, 25),
        "NUM_REAL": (Status.REDUZ, 25)
    },
    77: {
        "ID": (Status.REDUZ, 26),
        "FECHA_PAR": (Status.REDUZ, 26),
        "MENOS": (Status.REDUZ, 26),
        "NUM_REAL": (Status.REDUZ, 26)
    },
    78: {
        "ID": (Status.REDUZ, 27),
        "FECHA_PAR": (Status.REDUZ, 27),
        "MENOS": (Status.REDUZ, 27),
        "NUM_REAL": (Status.REDUZ, 27)
    },
    79: {
        "PONTOVIRG": (Status.SHIFT, 9)
    },
    80: {
        "PONTOVIRG": (Status.REDUZ, 3)
    },
    81: {
        "FECHAPHP": (Status.REDUZ, 2),
        "FECHA_CHAVE": (Status.REDUZ, 2)
    }

}

GOTO = {
    1: {
        "DC": 1,
        "VAR": 79,
        "VARS": 80,
        "CMDS": 17,
        "CMD_COND": 6,
        "CMD": 2
    },
    2: {
        "MAIS_CMDS": 16
    },
    5: {
        "MAIS_VAR": 15,
        "RESTO_IDENT": 12
    },
    6: {
        "DC": 16, 
        "CMDS": 56,
        "CMD_COND": 6,
        "CMD": 2
    },
    9: {
        "DC": 16,
        "CMDS": 22,
        "CMD_COND": 6
    },
    10: {
        "CONDICAO": 23,
        "EXPRESSAO": 57,
        "TERMO": 38,
        "OP_UN": 41
    },
    11: {
        "CONDICAO": 24,
        "EXPRESSAO": 57,
        "TERMO": 38,
        "OP_UN": 41
    },
    13: {
        "EXP_IDENT": 37,
        "EXPRESSAO": 60,
        "TERMO": 38,
        "OP_UN": 41
    },
    27: {
        "DC": 16,
        "CMDS": 32,
        "CMD_COND": 6,
        "CMD": 2
    },
    28: {
        "DC": 16,
        "CMDS": 29,
        "CMD_COND": 6,
        "CMD": 2
    },
    30: {
        "CMD": 31
    },
    35: {
        "DC": 16,
        "CMDS": 67,
        "CMD_COND": 6,
        "CMD": 2
    },
    36: {
        "MAIS_VAR": 15
    },
    38: {
        "OUTROS_TERMOS": 39,
        "OP_AD": 40
    },
    40: {
        "TERMO": 42,
        "OP_UN": 41
    },
    41: {
        "FATOR": 43
    },
    42: {
        "OUTROS_TERMOS": 44,
        "OP_AD": 40
    },
    43: {
        "MAIS_FATORES": 69,
        "OP_MUL": 70
    },
    49: {
        "EXPRESSAO": 51,
        "TERMO": 38,
        "OP_UN": 41
    },
    57: {
        "RELACAO": 58
    },
    58: {
        "EXPRESSAO": 59,
        "TERMO": 38,
        "OP_UN": 41
    },
    71: {
        "MAIS_FATORES": 72,
        "OP_MUL": 70
    },
    79: {
        "MAIS_CMDS": 81
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
    22: ("RELACAO", 2),
    23: ("RELACAO", 2),
    24: ("RELACAO", 2),
    25: ("RELACAO", 2),
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

def analisador_sintatico(tokens):
    pilha_estados = [0] 
    pilha_simbolos = []
    pilha_semantica = []
    i = 0
    acao = ""
    entrada = tokens
    entrada.append(None)
    while entrada:
        chave = entrada[0]
        if ACTION[pilha_estados[-1]][chave]:
            acao, estado = ACTION[pilha_estados[-1]][chave]
            if acao == Status.SHIFT:
                pilha_simbolos.append(entrada.pop(0))
                pilha_estados.append(estado)
            elif acao == Status.REDUZ:
                nome_subst, qtd_subst = GRAMATICA[estado]
                for i in range(qtd_subst):
                    pilha_estados.pop()
                    pilha_semantica.pop()
                    pilha_semantica.append(nome_subst)
