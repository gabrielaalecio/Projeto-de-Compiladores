import lexico, sintatico, maquina

with open('correto.php.txt') as arquivo:
    codigo = arquivo.read()

#Analisador Léxico
tokens = lexico.analisador_lexico(codigo)
if tokens is None:
    exit(1)

#Analisador Sintático - Ascendente
codigo_objeto = sintatico.analisador_sintatico(tokens)

with open("resultado.txt", "w", encoding="utf-8") as arquivo:
  for item in codigo_objeto:
    arquivo.write(f"{item}\n")

resultado = maquina.rodar_codigo()
