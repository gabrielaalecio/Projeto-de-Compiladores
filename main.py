import lexico, sintatico

with open('correto.php.txt') as arquivo:
    codigo = arquivo.read()

#Analisador Léxico
tokens = lexico.analisador_lexico(codigo)
if tokens is None:
    exit(1)

#Analisador Sintático - Ascendente
codigo_objeto = sintatico.analisador_sintatico(tokens)
