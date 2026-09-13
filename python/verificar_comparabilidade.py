from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------

# Caminho da base consolidada
ARQUIVO_DADOS = Path(
    "data/processed/BPS_20_26_BeatrizBruns.csv"
)

# Campos relevantes para comparação de preços
colunas_comparacao = [
    "co_catmat",
    "ds_item",
    "un_fornecimento",
    "vl_capacidade",
    "sg_unidade_medida",
    "no_fabricante",
    "vl_preco_unitario"
]


# ---------------------------------------------------------
# IMPORTAÇÃO DOS DADOS
# ---------------------------------------------------------

print("\nCarregando campos para análise de comparabilidade...")

dados = pd.read_csv(
    ARQUIVO_DADOS,
    sep=";",
    encoding="utf-8",
    usecols=colunas_comparacao,
    dtype={
        "co_catmat": "string"
    }
)

print("Dados carregados com sucesso.")


# ---------------------------------------------------------
# ANÁLISE DOS CAMPOS
# ---------------------------------------------------------

print(f"\n{'=' * 70}")
print("ANÁLISE DOS CAMPOS PARA COMPARAÇÃO DE PREÇOS")
print(f"{'=' * 70}")

# Exibe a quantidade de valores distintos de cada campo
for coluna in [
    "co_catmat",
    "un_fornecimento",
    "vl_capacidade",
    "sg_unidade_medida",
    "no_fabricante"
]:
    valores_distintos = dados[coluna].nunique(dropna=True)

    print(
        f"{coluna}: "
        f"{valores_distintos:,} valor(es) distinto(s)"
    )


# ---------------------------------------------------------
# COMPLETUDE DOS CAMPOS
# ---------------------------------------------------------

print(f"\n{'-' * 70}")
print("COMPLETUDE DOS CAMPOS")
print(f"{'-' * 70}")

for coluna in [
    "co_catmat",
    "un_fornecimento",
    "vl_capacidade",
    "sg_unidade_medida",
    "no_fabricante"
]:
    preenchidos = dados[coluna].notna().sum()

    percentual = (
        preenchidos / len(dados)
    ) * 100

    print(
        f"{coluna}: "
        f"{preenchidos:,} preenchidos "
        f"({percentual:.2f}%)"
    )


# ---------------------------------------------------------
# GRUPOS COM REGISTROS COMPARÁVEIS
# ---------------------------------------------------------

# Agrupa registros pelo mesmo CATMAT e
# pela mesma unidade de fornecimento.
grupos_comparaveis = (
    dados
    .dropna(
        subset=[
            "co_catmat",
            "un_fornecimento",
            "vl_preco_unitario"
        ]
    )
    .groupby(
        [
            "co_catmat",
            "un_fornecimento"
        ]
    )
    .size()
)


# Mantém somente grupos com pelo menos duas compras,
# pois é necessário haver mais de um registro para comparar preços.
grupos_com_mais_de_uma_compra = (
    grupos_comparaveis[
        grupos_comparaveis >= 2
    ]
)

print(f"\n{'-' * 70}")
print("POSSIBILIDADE DE COMPARAÇÃO")
print(f"{'-' * 70}")

print(
    "Grupos CATMAT + unidade de fornecimento "
    f"com pelo menos 2 registros: "
    f"{len(grupos_com_mais_de_uma_compra):,}"
)