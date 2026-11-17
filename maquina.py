def rodar_codigo():
    with open('resultado.txt') as arquivo:
        codigo = arquivo.read().split("\n")

    lista_vars = []
    aux = []
    pilha_carregada = []

    for c in codigo:
        codigo_valor = c.split(" ")
        match codigo_valor[0]:
            case "PARA":
                print("return 0")
            case "ALME":
                lista_vars.append(None)
            case "CRCT":
                aux.append(int(codigo_valor[1]))
            case "CRVL":
                aux.append(lista_vars[int(codigo_valor[1])])
            case "SOMA":
                result = sum(aux)
                aux.clear()
            case "SUBT":
                print("")
            case "MULT":
                print("")
            case "DIVI":
                print("")
            case "INVE":
                print("")
            case "CONJ":
                print("")
            case "DISJ":
                print("")
            case "NEGA":
                print("")
            case "CPME":
                print("")
            case "CPMA":
                print("")
            case "CPIG":
                print("")
            case "CDES":
                print("")
            case "CPMI":
                print("")
            case "CMAI":
                print("")
            case "ARMZ":
                lista_vars[int(codigo_valor[1])] = result
            case "LEIT":
                print("")
            case "IMPR":
                print(aux.pop())
            case "INPP":
                print("")