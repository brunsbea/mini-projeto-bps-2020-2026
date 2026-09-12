from pathlib import Path
import pandas as pd

# Define a pasta onde estão armazenadas as bases originais do BPS
PASTA_DADOS = Path("data/raw")

# Define os anos que serão processados
anos = range(2020, 2027)

# Variável utilizada para somar a quantidade de registros de todas as bases
total_registros = 0


# Percorre cada arquivo anual do BPS
for ano in anos:

    # Monta o caminho do arquivo correspondente ao ano
    arquivo = PASTA_DADOS / f"BPS_{ano}.csv"

    print(f"\n{'=' * 70}")
    print(f"DIAGNÓSTICO DA BASE DE {ano}")
    print(f"{'=' * 70}")

    # Importa a base anual completa
    dados = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8"
    )

    # Conta a quantidade de registros da base
    quantidade_registros = len(dados)

    # Soma os registros para conferência posterior da base consolidada
    total_registros += quantidade_registros

    print(f"\nQuantidade de linhas: {quantidade_registros:,}")
    print(f"Quantidade de colunas: {len(dados.columns)}")

    # Verifica os anos existentes na coluna ano_compra
    print(f"Ano(s) encontrado(s): {dados['ano_compra'].unique()}")

    # Verifica a quantidade de registros completamente duplicados
    quantidade_duplicados = dados.duplicated().sum()

    print(f"\nRegistros completamente duplicados: {quantidade_duplicados:,}")

    # Calcula a quantidade de valores nulos em cada coluna
    valores_nulos = dados.isnull().sum()

    # Mantém somente as colunas que possuem pelo menos um valor nulo
    valores_nulos = valores_nulos[valores_nulos > 0]

    print("\nColunas com valores nulos:")

    if valores_nulos.empty:
        print("Nenhum valor nulo identificado.")
    else:
        for coluna, quantidade in valores_nulos.items():

            # Calcula o percentual de valores nulos na coluna
            percentual = (quantidade / quantidade_registros) * 100

            print(
                f"{coluna}: {quantidade:,} "
                f"({percentual:.2f}%)"
            )

    # Libera a variável antes de carregar o arquivo seguinte
    del dados


# Exibe a quantidade total de registros encontrados
print(f"\n{'=' * 70}")
print("RESUMO GERAL")
print(f"{'=' * 70}")
print(f"Total de registros entre 2020 e 2026: {total_registros:,}")