import re

def analisar_linha(linha, numero_linha):
    # Expressão regular para verificar se é uma linha de atribuição
    padrao_atribuicao = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9]*)\s*=\s*(".*?"|\d+\.\d+|\d+)$')

    # Expressão regular para verificar se é uma linha de função
    padrao_funcao = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9]*)\s*,\s*([a-zA-Z][a-zA-Z0-9]*)(\s*,\s*("[^"]*"|\d+\.\d+|\d+))*$')

    # Verifica se é uma linha de atribuição
    match_atribuicao = padrao_atribuicao.match(linha)
    if match_atribuicao:
        nome_variavel=match_atribuicao.group(1)
        tipo,  valor = determinar_tipo_valor(match_atribuicao.group(2))
        relatorio = f"{tipo},{nome_variavel},{valor}"
        print(relatorio)
    else:
        # Verifica se é uma linha de função
        match_funcao = padrao_funcao.match(linha)
        if match_funcao:
            print("*" * 20)
            print(f"function:{match_funcao.group(1)}")
            parametros = match_funcao.groups()
            for parametro in parametros:
               
                if parametro!=None:
                    tipo, valor = determinar_tipo_valor(parametro)
                    print(f"{tipo},{valor}")
            print("*" * 20)
        else:
            print(f"erro:linha {numero_linha}")

def determinar_tipo_valor(valor):
    # Determina o tipo e valor da variável
    if '"' in valor:
        return "string", valor
    elif valor[0].isalpha():
        return "variable",  valor
    elif "." in valor:
        return "float", float(valor)
    else:
        return "int", int(valor)

def analisar_codigo(arquivo):
    with open(arquivo, 'r') as f:
        for numero_linha, linha in enumerate(f, start=1):
            analisar_linha(linha.strip(), numero_linha)


print("\x1bc\x1b[43;37m")
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python analisador.py arquivo.macro")
        sys.exit(1)

    arquivo_a_analisar = sys.argv[1]
    analisar_codigo(arquivo_a_analisar)

