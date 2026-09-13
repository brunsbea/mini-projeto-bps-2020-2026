from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------

# Define o caminho da base consolidada
ARQUIVO_DADOS = Path(
    "data/processed/BPS_20_26_BeatrizBruns.csv"
)

# Define somente as colunas necessárias para calcular os KPIs.
# Isso evita carregar todas as 36 colunas na memória.
colunas_necessarias = [
    "cnpj_instituicao",
    "cnpj_fornecedor",
    "qt_medicamento",
    "vl_preco_unitario",
    "vl_preco_total"
]


# ---------------------------------------------------------
# IMPORTAÇÃO DOS DADOS
# ---------------------------------------------------------

print("\nCarregando a base consolidada...")

dados = pd.read_csv(
    ARQUIVO_DADOS,
    sep=";",
    encoding="utf-8",
    usecols=colunas_necessarias,
    dtype={
        "cnpj_instituicao": "string",
        "cnpj_fornecedor": "string"
    }
)

print("Base carregada com sucesso.")


# ---------------------------------------------------------
# GARANTIA DOS TIPOS NUMÉRICOS
# ---------------------------------------------------------

# Garante que os campos utilizados nos cálculos
# estejam armazenados como números.
dados["qt_medicamento"] = pd.to_numeric(
    dados["qt_medicamento"],
    errors="coerce"
)

dados["vl_preco_unitario"] = pd.to_numeric(
    dados["vl_preco_unitario"],
    errors="coerce"
)

dados["vl_preco_total"] = pd.to_numeric(
    dados["vl_preco_total"],
    errors="coerce"
)


# ---------------------------------------------------------
# CÁLCULO DOS KPIs OBRIGATÓRIOS
# ---------------------------------------------------------

# KPI 1 - Valor total registrado
# Soma todos os valores registrados nas compras.
valor_total = dados["vl_preco_total"].sum()

# KPI 2 - Quantidade total de itens comprados
# Soma todas as quantidades adquiridas.
quantidade_total = dados["qt_medicamento"].sum()

# KPI 3 - Número de registros de compra
# Conta a quantidade de linhas da base consolidada.
numero_registros = len(dados)

# KPI 4 - Instituições compradoras
# Conta quantos CNPJs de instituições diferentes existem.
instituicoes_compradoras = dados[
    "cnpj_instituicao"
].nunique(dropna=True)

# KPI 5 - Fornecedores
# Conta quantos CNPJs de fornecedores diferentes existem.
fornecedores = dados[
    "cnpj_fornecedor"
].nunique(dropna=True)

# KPI 6 - Preço unitário médio ponderado
# Divide o valor total registrado pela quantidade total adquirida.
preco_medio_ponderado = (
    valor_total / quantidade_total
)


# ---------------------------------------------------------
# MÉTRICAS AUXILIARES
# ---------------------------------------------------------

# Calcula a média simples do preço unitário apenas para comparação.
# Ela NÃO substitui o KPI de preço médio ponderado.
preco_unitario_medio_simples = dados[
    "vl_preco_unitario"
].mean()

# Calcula a mediana dos preços unitários.
# A mediana pode ajudar a analisar distribuições com valores extremos.
mediana_preco_unitario = dados[
    "vl_preco_unitario"
].median()


# ---------------------------------------------------------
# EXIBIÇÃO DOS RESULTADOS
# ---------------------------------------------------------

print(f"\n{'=' * 70}")
print("KPIs - BPS 2020 A 2026")
print(f"{'=' * 70}")

print(f"Valor total registrado: R$ {valor_total:,.2f}")
print(f"Quantidade total de itens: {quantidade_total:,.0f}")
print(f"Número de registros: {numero_registros:,}")
print(f"Instituições compradoras: {instituicoes_compradoras:,}")
print(f"Fornecedores: {fornecedores:,}")
print(
    f"Preço unitário médio ponderado: "
    f"R$ {preco_medio_ponderado:,.4f}"
)

print(f"\n{'-' * 70}")
print("MÉTRICAS AUXILIARES")
print(f"{'-' * 70}")

print(
    f"Preço unitário médio simples: "
    f"R$ {preco_unitario_medio_simples:,.4f}"
)

print(
    f"Mediana do preço unitário: "
    f"R$ {mediana_preco_unitario:,.4f}"
)