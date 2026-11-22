def rodar_codigo():
    with open('resultado.txt') as arquivo:
        codigo = arquivo.read().split("\n")
    indice = 0
    lista_vars = []
    pilha = []
    while indice < len(codigo):
        codigo_valor = codigo[indice].split(" ")
        comando = codigo_valor[0]
        valor = int(codigo_valor[1]) if isinstance(codigo_valor, (list, tuple)) and len(codigo_valor) > 1 else 0
        if comando in ["SOMA", "SUBT", "MULT", "DIVI","CPME", "CPMA","CPIG","CDES", "CPMI", "CMAI", "DISJ", "CONJ"]:
            valor_dois = pilha.pop()
            valor_um = pilha.pop()

        match comando:
            case "INPP":
                pass
            case "PARA":
                return
            case "ALME":
                for i in range(valor):
                    lista_vars.append(None)
            case "CRCT":
                pilha.append(valor)
            case "CRVL":
                pilha.append(lista_vars[valor])
            case "SOMA":
                pilha.append(valor_um + valor_dois)
            case "SUBT":
                pilha.append(valor_um - valor_dois)
            case "MULT":
                pilha.append(valor_um * valor_dois)
            case "DIVI":
                pilha.append(valor_um / valor_dois)
            case "INVE":
                pilha.append(pilha.pop() * -1)
            case "CONJ":
                pilha.append(valor_um and valor_dois)
            case "DISJ":
                pilha.append(valor_um or valor_dois)
            case "NEGA":
                pilha[-1] = not pilha[-1]
            case "CPME":
                pilha.append(valor_um < valor_dois)
            case "CPMA":
                pilha.append(valor_um > valor_dois)
            case "CPIG":
                pilha.append(valor_um == valor_dois)
            case "CDES":
                pilha.append(valor_um != valor_dois)
            case "CPMI":
                pilha.append(valor_um <= valor_dois)
            case "CMAI":
                pilha.append(valor_um >= valor_dois)
            case "ARMZ":
                lista_vars[valor] = pilha.pop()
            case "LEIT":
                pilha.append(float(input()))
            case "IMPR":
                print(pilha.pop())
            case "DSVF":
                if not pilha.pop():
                    indice = valor - 1
                    continue
            case "DSVI":
                indice = valor - 1
                continue
        indice = indice + 1