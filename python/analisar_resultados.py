from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------

# Define o caminho da base consolidada
ARQUIVO_DADOS = Path(
    "data/processed/BPS_20_26_BeatrizBruns.csv"
)


# ---------------------------------------------------------
# IMPORTAÇÃO DOS DADOS
# ---------------------------------------------------------

print("\nCarregando a base consolidada...")

dados = pd.read_csv(
    ARQUIVO_DADOS,
    sep=";",
    encoding="utf-8",
    dtype={
        "cnpj_instituicao": "string",
        "cnpj_fornecedor": "string",
        "cnpj_fabricante": "string",
        "co_catmat": "string"
    }
)

print(f"Registros carregados: {len(dados):,}")


# ---------------------------------------------------------
# 1. EVOLUÇÃO ANUAL
# ---------------------------------------------------------

evolucao_anual = (
    dados
    .groupby("ano_compra")
    .agg(
        valor_total=("vl_preco_total", "sum"),
        quantidade_total=("qt_medicamento", "sum"),
        registros=("co_seq_bps", "count")
    )
    .reset_index()
)

print(f"\n{'=' * 70}")
print("EVOLUÇÃO ANUAL")
print(f"{'=' * 70}")
print(evolucao_anual.to_string(index=False))


# ---------------------------------------------------------
# 2. TOP 10 ESTADOS
# ---------------------------------------------------------

top_estados = (
    dados
    .groupby("sg_uf")["vl_preco_total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(f"\n{'=' * 70}")
print("TOP 10 ESTADOS POR VALOR TOTAL")
print(f"{'=' * 70}")
print(top_estados)


# ---------------------------------------------------------
# 3. TOP 10 MUNICÍPIOS
# ---------------------------------------------------------

# Utiliza UF + município para evitar que municípios
# com o mesmo nome em estados diferentes sejam agrupados.
top_municipios = (
    dados
    .groupby(
        ["sg_uf", "no_municipio"],
        as_index=False
    )["vl_preco_total"]
    .sum()
    .sort_values(
        "vl_preco_total",
        ascending=False
    )
    .head(10)
)

print(f"\n{'=' * 70}")
print("TOP 10 MUNICÍPIOS POR VALOR TOTAL")
print(f"{'=' * 70}")
print(top_municipios.to_string(index=False))


# ---------------------------------------------------------
# 4. TOP 10 INSTITUIÇÕES
# ---------------------------------------------------------

# Utiliza CNPJ + nome para distinguir corretamente
# instituições que possuem nomes iguais ou semelhantes.
top_instituicoes = (
    dados
    .groupby(
        ["cnpj_instituicao", "no_instituicao"],
        as_index=False
    )["vl_preco_total"]
    .sum()
    .sort_values(
        "vl_preco_total",
        ascending=False
    )
    .head(10)
)

print(f"\n{'=' * 70}")
print("TOP 10 INSTITUIÇÕES POR VALOR TOTAL")
print(f"{'=' * 70}")
print(top_instituicoes.to_string(index=False))


# ---------------------------------------------------------
# 5. TOP 10 PRODUTOS POR VALOR
# ---------------------------------------------------------

top_produtos_valor = (
    dados
    .groupby(["co_catmat", "ds_item"])["vl_preco_total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(f"\n{'=' * 70}")
print("TOP 10 PRODUTOS POR VALOR TOTAL")
print(f"{'=' * 70}")
print(top_produtos_valor)


# ---------------------------------------------------------
# 6. TOP 10 PRODUTOS POR QUANTIDADE
# ---------------------------------------------------------

top_produtos_quantidade = (
    dados
    .groupby(["co_catmat", "ds_item"])["qt_medicamento"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(f"\n{'=' * 70}")
print("TOP 10 PRODUTOS POR QUANTIDADE")
print(f"{'=' * 70}")
print(top_produtos_quantidade)


# ---------------------------------------------------------
# 7. TOP 10 FORNECEDORES
# ---------------------------------------------------------

# Utiliza CNPJ + nome para que cada fornecedor
# seja identificado de forma individual.
top_fornecedores = (
    dados
    .groupby(
        ["cnpj_fornecedor", "no_fornecedor"],
        as_index=False
    )["vl_preco_total"]
    .sum()
    .sort_values(
        "vl_preco_total",
        ascending=False
    )
    .head(10)
)

print(f"\n{'=' * 70}")
print("TOP 10 FORNECEDORES POR VALOR TOTAL")
print(f"{'=' * 70}")
print(top_fornecedores.to_string(index=False))


# ---------------------------------------------------------
# 8. TOP 10 FABRICANTES
# ---------------------------------------------------------

# Utiliza CNPJ + nome para distinguir fabricantes
# que possam possuir nomes iguais ou semelhantes.
top_fabricantes = (
    dados
    .groupby(
        ["cnpj_fabricante", "no_fabricante"],
        as_index=False
    )["vl_preco_total"]
    .sum()
    .sort_values(
        "vl_preco_total",
        ascending=False
    )
    .head(10)
)

print(f"\n{'=' * 70}")
print("TOP 10 FABRICANTES POR VALOR TOTAL")
print(f"{'=' * 70}")
print(top_fabricantes.to_string(index=False))


# ---------------------------------------------------------
# 9. MODALIDADES DE COMPRA
# ---------------------------------------------------------

modalidades = (
    dados
    .groupby("modalidade")["vl_preco_total"]
    .sum()
    .sort_values(ascending=False)
)

print(f"\n{'=' * 70}")
print("VALOR TOTAL POR MODALIDADE")
print(f"{'=' * 70}")
print(modalidades)


# ---------------------------------------------------------
# 10. INVESTIGAÇÃO DE PREÇOS DE PRODUTO COMPARÁVEL
# ---------------------------------------------------------

# Produto escolhido para a investigação:
# CATMAT 271089 - Amoxicilina 500 mg
#
# Além do CATMAT, restringimos a unidade de fornecimento
# para evitar comparar apresentações diferentes.

catmat_analise = "271089"
unidade_analise = "COMPRIMIDO"

comparacao_preco = dados[
    (dados["co_catmat"].astype("string") == catmat_analise)
    & (
        dados["un_fornecimento"]
        .astype("string")
        .str.strip()
        .str.upper()
        == unidade_analise
    )
].copy()

print(f"\n{'=' * 70}")
print("INVESTIGAÇÃO DE PREÇOS - AMOXICILINA 500 MG")
print(f"{'=' * 70}")

print(f"CATMAT: {catmat_analise}")
print(f"Unidade de fornecimento: {unidade_analise}")
print(f"Registros encontrados: {len(comparacao_preco):,}")

print(
    "Fornecedores distintos:",
    comparacao_preco["cnpj_fornecedor"].nunique()
)

print(
    "Anos encontrados:",
    sorted(comparacao_preco["ano_compra"].unique())
)

print(
    "UFs encontradas:",
    sorted(comparacao_preco["sg_uf"].dropna().unique())
)


# Estatísticas gerais do preço unitário
print("\nResumo do preço unitário:")

print(
    f"Preço mínimo: "
    f"R$ {comparacao_preco['vl_preco_unitario'].min():,.4f}"
)

print(
    f"Preço mediano: "
    f"R$ {comparacao_preco['vl_preco_unitario'].median():,.4f}"
)

print(
    f"Preço médio simples: "
    f"R$ {comparacao_preco['vl_preco_unitario'].mean():,.4f}"
)

print(
    f"Preço máximo: "
    f"R$ {comparacao_preco['vl_preco_unitario'].max():,.4f}"
)

# ---------------------------------------------------------
# DISTRIBUIÇÃO DOS REGISTROS POR ANO E UF
# ---------------------------------------------------------

# Antes de comparar fornecedores diretamente, verificamos
# em quais combinações de ano e UF existem mais registros.
#
# Isso ajuda a escolher grupos mais comparáveis em relação
# ao período e à localização.

registros_ano_uf = (
    comparacao_preco
    .groupby(
        ["ano_compra", "sg_uf"],
        as_index=False
    )
    .agg(
        registros=("co_seq_bps", "count"),
        fornecedores=("cnpj_fornecedor", "nunique")
    )
    .sort_values(
        ["registros", "fornecedores"],
        ascending=False
    )
    .head(10)
)

print("\nPrincipais combinações de ano e UF:")
print(registros_ano_uf.to_string(index=False))


# ---------------------------------------------------------
# 11. COMPARAÇÃO DE PREÇOS EM RECORTE MAIS HOMOGÊNEO
# ---------------------------------------------------------

# A combinação 2021 + PI foi escolhida porque apresentou
# a maior quantidade de registros para a Amoxicilina 500 mg
# em comprimidos, além de possuir vários fornecedores.
#
# Mesmo assim, os resultados devem ser interpretados como
# investigação, pois fabricante, instituição, modalidade,
# quantidade e condições de negociação podem influenciar
# os preços registrados.

ano_analise = 2021
uf_analise = "PI"

comparacao_recorte = comparacao_preco[
    (comparacao_preco["ano_compra"] == ano_analise)
    & (comparacao_preco["sg_uf"] == uf_analise)
].copy()


print(f"\n{'=' * 70}")
print("COMPARAÇÃO DE PREÇOS - AMOXICILINA 500 MG")
print(f"{'=' * 70}")

print(f"Ano: {ano_analise}")
print(f"UF: {uf_analise}")
print(f"Unidade de fornecimento: {unidade_analise}")
print(f"Registros analisados: {len(comparacao_recorte):,}")

print(
    "Fornecedores distintos:",
    comparacao_recorte["cnpj_fornecedor"].nunique()
)

print(
    "Instituições distintas:",
    comparacao_recorte["cnpj_instituicao"].nunique()
)

print(
    "Fabricantes distintos:",
    comparacao_recorte["cnpj_fabricante"].nunique()
)


# ---------------------------------------------------------
# RESUMO POR FORNECEDOR
# ---------------------------------------------------------

# Calcula estatísticas por fornecedor.
# A média ponderada considera a quantidade adquirida
# em cada registro:
#
# soma do valor total / soma da quantidade

precos_fornecedor = (
    comparacao_recorte
    .groupby(
        ["cnpj_fornecedor", "no_fornecedor"],
        as_index=False
    )
    .agg(
        registros=("co_seq_bps", "count"),
        quantidade_total=("qt_medicamento", "sum"),
        valor_total=("vl_preco_total", "sum"),
        preco_minimo=("vl_preco_unitario", "min"),
        preco_mediano=("vl_preco_unitario", "median"),
        preco_maximo=("vl_preco_unitario", "max"),
        instituicoes=("cnpj_instituicao", "nunique"),
        fabricantes=("cnpj_fabricante", "nunique"),
        modalidades=("modalidade", "nunique")
    )
)

# Preço médio ponderado por fornecedor
precos_fornecedor["preco_medio_ponderado"] = (
    precos_fornecedor["valor_total"]
    / precos_fornecedor["quantidade_total"]
)

# Organiza do menor para o maior preço médio ponderado
precos_fornecedor = precos_fornecedor.sort_values(
    "preco_medio_ponderado"
)


print("\nResumo por fornecedor:")

print(
    precos_fornecedor[
        [
            "no_fornecedor",
            "registros",
            "quantidade_total",
            "preco_minimo",
            "preco_mediano",
            "preco_medio_ponderado",
            "preco_maximo",
            "instituicoes",
            "fabricantes",
            "modalidades"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# RESUMO GERAL DO RECORTE
# ---------------------------------------------------------

print("\nResumo geral do recorte:")

print(
    f"Preço mínimo: "
    f"R$ {comparacao_recorte['vl_preco_unitario'].min():,.4f}"
)

print(
    f"Preço mediano: "
    f"R$ {comparacao_recorte['vl_preco_unitario'].median():,.4f}"
)

print(
    f"Preço máximo: "
    f"R$ {comparacao_recorte['vl_preco_unitario'].max():,.4f}"
)

preco_ponderado_recorte = (
    comparacao_recorte["vl_preco_total"].sum()
    / comparacao_recorte["qt_medicamento"].sum()
)

print(
    f"Preço médio ponderado: "
    f"R$ {preco_ponderado_recorte:,.4f}"
)

# ---------------------------------------------------------
# 12. RESUMO FINAL
# ---------------------------------------------------------

print(f"\n{'=' * 70}")
print("RESUMO")
print(f"{'=' * 70}")

print(
    f"Ano com maior valor total: "
    f"{evolucao_anual.loc[evolucao_anual['valor_total'].idxmax(), 'ano_compra']}"
)

print(
    f"Estado com maior valor total: "
    f"{top_estados.index[0]}"
)

print(
    f"Município com maior valor total: "
    f"{top_municipios.iloc[0]['no_municipio']} "
    f"({top_municipios.iloc[0]['sg_uf']})"
)

print(
    f"Modalidade com maior valor total: "
    f"{modalidades.index[0]}"
)