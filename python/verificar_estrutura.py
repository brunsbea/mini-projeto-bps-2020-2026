from pathlib import Path
import pandas as pd

# Define a pasta onde estão armazenadas as bases anuais do BPS
PASTA_DADOS = Path("data/raw")

# Define o intervalo de anos que será analisado
anos = range(2020, 2027)

# Cria um dicionário para armazenar as colunas de cada ano
estruturas = {}


# Percorre cada ano da base do BPS
for ano in anos:

    # Monta o caminho do arquivo correspondente ao ano
    arquivo = PASTA_DADOS / f"BPS_{ano}.csv"

    # Lê somente o cabeçalho do arquivo, pois queremos analisar apenas a estrutura das colunas
    dados = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
        nrows=0
    )

    # Armazena a lista de colunas encontrada naquele ano
    estruturas[ano] = list(dados.columns)


# Define 2020 como a estrutura de referência para comparação
estrutura_referencia = estruturas[2020]


print("\n" + "=" * 60)
print("COMPARAÇÃO DA ESTRUTURA DAS BASES")
print("=" * 60)

# Exibe a quantidade de colunas encontrada em cada ano
print("\nQuantidade de colunas por ano:")

for ano in anos:
    print(f"{ano}: {len(estruturas[ano])} colunas")


# Compara cada ano com a estrutura de referência de 2020
print("\nComparação com a estrutura de 2020:")

for ano in anos:
    
    # Verifica se as colunas e a ordem são exatamente iguais
    estrutura_igual = estruturas[ano] == estrutura_referencia

    if estrutura_igual:
        print(f"{ano}: OK - estrutura igual a 2020")
    else:
        print(f"{ano}: DIFERENTE - estrutura precisa ser investigada")


# Verifica se todas as bases possuem exatamente a mesma estrutura
todas_iguais = all(
    estruturas[ano] == estrutura_referencia
    for ano in anos
)


print("\n" + "=" * 60)

if todas_iguais:
    print("RESULTADO FINAL: todas as bases possuem a mesma estrutura.")
else:
    print("RESULTADO FINAL: existem diferenças entre as estruturas.")

print("=" * 60)