import re
def executar_operacao(match):
    if match==None:
        return ""
    
    
    operando1,operacao, operando2 = re.match(r'([0-9]{1,}\.[0-9]{1,})([+\-*\/])([0-9]{1,}\.[0-9]{1,})', match).groups()
    operando1, operando2 = float(operando1), float(operando2)

    if operacao == '+':
        return f'add {operando1},{operando2}\n'
    elif operacao == '-':
        return f'sub {operando1},{operando2}\n'
    elif operacao == '*':
        return f'mul {operando1},{operando2}\n'
    elif operacao == '/':
        return f'div {operando1},{operando2}\n'


def analisar_expressao(expressao):
    # Remove espaços em branco
    expressao = expressao.replace(" ", "")

    # Encontra expressões entre parênteses mais internos
    while "(" in expressao:
        expressao = re.sub(r'\(([^()]*)\)', lambda match: str(analisar_expressao(match.group(1))), expressao)

    # Encontra multiplicação e divisão
    padrao_mult_div = re.compile(r'(\d+\.?\d*)[*/](\d+\.?\d*)')
    while re.search(padrao_mult_div, expressao):
        expressao = re.sub(padrao_mult_div, lambda match: executar_operacao(match.group(0)), expressao, count=1)

    # Encontra soma e subtração
    padrao_soma_sub = re.compile(r'(\d+\.?\d*)[+\-](\d+\.?\d*)')
    while re.search(padrao_soma_sub, expressao):
        expressao = re.sub(padrao_soma_sub, lambda match: executar_operacao(match.group(0)), expressao, count=1)

    return expressao

def analisar_linha(linha, numero_linha):
    # Expressão regular para verificar se é uma linha de atribuição
    padrao_atribuicao = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9]*)\s*=\s*(".*?"|\d+\.\d+|\d+)$')
    padrao_atribuicao2 = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9]*)\s*=(.*?)$')
    # Expressão regular para verificar se é uma linha de função
    padrao_funcao = re.compile(r"[a-zA-Z0-9_]+(?:[\\s,]+[a-zA-Z0-9_])*")

    # Verifica se é uma linha de atribuição
    match_atribuicao = padrao_atribuicao.match(linha)
    match_atribuicao2 = padrao_funcao.match(linha)
    values=linha.find("=")

    if match_atribuicao:
        nome_variavel=match_atribuicao.group(1)
        tipo,valor = determinar_tipo_valor(match_atribuicao.group(2))
        relatorio = f"{tipo},{nome_variavel},{valor}"
        print(relatorio)
    elif values<0:
        # Verifica se é uma linha de função
        match_funcao = padrao_funcao.match(linha)
        if match_funcao:
            print("*" * 20)
            
            print(f"function:{match_funcao.group(0)}")
            parametros = re.findall(r"[a-zA-Z0-9_]+(?:[\\s,]+[a-zA-Z0-9_])*",linha)
           
            for parametro in parametros:
               
                if parametro!=None:
                    tipo, valor = determinar_tipo_valor(parametro)
                    print(f"{tipo},{valor}")
            print("*" * 20)
        else:
            print(f"erro:linha {numero_linha}")
    else:
        match_atribuicao2 = padrao_atribuicao2.match(linha)
        nome_variavel=match_atribuicao2.group(1)
        valores=match_atribuicao2.group(2)
        
        valor = analisar_expressao(valores)
   
        relatorio = f"float,{nome_variavel},{valor}"
        print(relatorio)

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

