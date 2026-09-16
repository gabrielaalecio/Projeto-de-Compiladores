import lexico, sintatico, semantico

with open('correto.php.txt') as arquivo:
    codigo = arquivo.read()

#Análisador Léxico
tokens = lexico.analisador_lexico(codigo)

#Analisador Sintático - Ascendente
codigo_objeto = sintatico.analisador_sintatico(tokens)

#Analisador Semântico
resultado = semantico.analisador_semantico(codigo_objeto)