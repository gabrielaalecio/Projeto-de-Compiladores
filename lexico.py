import re

token_specs = [
    ('ABREPHP',     r'<\?php'),
    ('FECHAPHP',    r'\?>'),
    ('PHP_EOL',     r'PHP_EOL'),
    ('FLOATVAL',    r'floatval'),
    ('READLINE',    r'readline'),
    ('IF',          r'\bif\b'),
    ('ELSE',        r'\belse\b'),
    ('WHILE',       r'\bwhile\b'),
    ('ECHO',        r'\becho\b'),
    ('NUM_REAL',    r'\d+\.\d+|\d+'),
    ('ID',          r'\$[a-zA-Z_][a-zA-Z0-9_]*'),
    ('IGUAL_IGUAL', r'=='),
    ('DIFERENTE',   r'!='),
    ('MAIOR_IGUAL', r'>='),
    ('MENOR_IGUAL', r'<='),
    ('MAIOR',       r'>'),
    ('MENOR',       r'<'),
    ('ATRIB',       r'='),
    ('MAIS',        r'\+'),
    ('MENOS',       r'-'),
    ('MULT',        r'\*'),
    ('DIV',         r'/'),
    ('PONTO',       r'\.'),
    ('VIRGULA',     r','),
    ('PONTOVIRG',   r';'),
    ('ABRE_PAR',    r'\('),
    ('FECHA_PAR',   r'\)'),
    ('ABRE_CHAVE',  r'\{'),
    ('FECHA_CHAVE', r'\}'),
    ('ESPACO',      r'[ \t\n]+'),
    ('DESCONHECIDO', r'.'),
]

regex_geral = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in token_specs)
padrao_compilado = re.compile(regex_geral)

unicos = []

def contar_linhas(codigo, ponto_parada):
    contador = conta_letra = 0
    for i in range(ponto_parada):
        conta_letra = conta_letra + 1
        if codigo[i] == '\n':
            conta_letra = 0
            contador += 1
    return contador + 1, conta_letra + 1

def analisador_lexico(codigo):
    tokens = []
    for match in padrao_compilado.finditer(codigo):
        tipo = match.lastgroup
        lexema = match.group()
    
        if tipo == 'ESPACO':
            continue
        elif tipo == 'DESCONHECIDO':
            linha, posicao = contar_linhas(codigo, match.start())
            erro = f"Caractere inválido: '{lexema}' na linha {linha}, posição {posicao}"
            print(erro)
            return

        if tipo == 'ID' or tipo == 'NUM_REAL':
            if lexema not in unicos:
                unicos.append(lexema)

        tokens.append((tipo, lexema))
    return tokens

