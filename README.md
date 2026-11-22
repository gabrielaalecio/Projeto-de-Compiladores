# Compilador de um subconjunto de PHP

Esse é um projeto de compilador feito em Python desenvolvido para concluir a matéria Projeto de Compiladores, ministrada pelo Prof. Dr. Raphael De Souza Rosa Gomes.
Ele lê um programa escrito em um subconjunto de PHP, faz a análise léxica, análise sintática ascendente (SLR) e análise semântica, gera o código objeto para uma máquina e executa esse código.

## Como preparar o ambiente

* Tenha o Python instalado na máquina (versão 3.10 ou superior, pois o projeto usa `match/case`);
* Não é necessário instalar nenhuma biblioteca externa;

## Arquivos do projeto

| Arquivo | Função |
|---|---|
| `lexico.py` | Analisador léxico: transforma o código-fonte em uma lista de tokens |
| `sintatico.py` | Analisador sintático ascendente (tabela SLR) e gerador do código objeto |
| `maquina.py` | Máquina de pilha que executa o código objeto |
| `main.py` | Liga as etapas: léxico, sintático e máquina |
| `correto.php.txt` | Programa de entrada (o `main.py` lê exatamente esse nome) |
| `resultado.txt` | Código objeto gerado (criado a cada execução) |

## Como rodar

* Escreva o programa que deseja compilar no arquivo `correto_php.txt`.
* Rode o arquivo `main.py` com o seguinte comando:

```
python main.py
```

Para executar de novo o `resultado.txt` já gerado, sem compilar outra vez:

```
python -c "import maquina; maquina.rodar_codigo()"
```

## Exemplo

Conteúdo do `correto.php.txt`:

```php
<?php
$cont;
$a,$b,$c;
$cont = 10;
while ($cont > 0) {
  $a = floatval(readline());
  $b = floatval(readline());
  if ($a > $b) {
    $c = - $a - $b;
  } else {
    $c = $b - $a;
  }
  echo $c . PHP_EOL;
  $cont = $cont - 1;
}
  echo $c . PHP_EOL;
?>
```

O programa lê 10 pares de números (`$a` e `$b`) e, para cada par, imprime `-$a - $b` se `$a > $b`, ou `$b - $a` caso contrário.
No fim, imprime de novo o último resultado. Entrada e saída de exemplo (digite um número por linha):

| `$a` | `$b` | Saída esperada |
|---|---|---|
| 5 | 3 | `-8.0` |
| 2 | 8 | `6.0` |
| 1 | 1 | `0.0` |
| 9 | 7 | `-16.0` |

Trecho do `resultado.txt` gerado (início do programa e do laço):

```
INPP
ALME 1
ALME 1
ALME 1
ALME 1
CRCT 10
ARMZ 0
CRVL 0
CRCT 0
CPMA
DSVF 37
...
