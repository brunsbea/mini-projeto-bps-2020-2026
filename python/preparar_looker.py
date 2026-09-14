from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------

# Base consolidada completa do projeto
ARQUIVO_ENTRADA = Path(
    "data/processed/BPS_20_26_BeatrizBruns.csv"
)

# Pasta destinada aos arquivos auxiliares do dashboard
PASTA_SAIDA = Path("data/looker")

# Arquivo otimizado que será enviado ao Data Studio
ARQUIVO_SAIDA = (
    PASTA_SAIDA / "BPS_Looker_2020_2026.csv"
)

# Cria a pasta de saída caso ela ainda não exista
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# LIMPEZA DOS ARQUIVOS AUXILIARES ANTERIORES
# ---------------------------------------------------------

# Remove versões anteriores dos arquivos para o Data Studio,
# evitando que arquivos antigos fiquem misturados na pasta.
for arquivo in PASTA_SAIDA.glob("BPS_Looker_*.csv"):
    arquivo.unlink()


# ---------------------------------------------------------
# COLUNAS NECESSÁRIAS DA BASE ORIGINAL
# ---------------------------------------------------------

# Carrega somente os campos necessários para construir
# os KPIs, filtros e visuais do dashboard.
colunas_necessarias = [
    "ano_compra",
    "cnpj_instituicao",
    "no_instituicao",
    "sg_uf",
    "no_municipio",
    "co_catmat",
    "ds_item",
    "un_fornecimento",
    "cnpj_fornecedor",
    "no_fornecedor",
    "no_fabricante",
    "modalidade",
    "qt_medicamento",
    "vl_preco_unitario",
    "vl_preco_total"
]


# ---------------------------------------------------------
# LEITURA DA BASE
# ---------------------------------------------------------

print("\nCarregando a base consolidada...")

dados = pd.read_csv(
    ARQUIVO_ENTRADA,
    sep=";",
    encoding="utf-8",
    usecols=colunas_necessarias,
    dtype={
        "cnpj_instituicao": "string",
        "cnpj_fornecedor": "string",
        "co_catmat": "string"
    }
)

print(f"Registros carregados: {len(dados):,}")


# ---------------------------------------------------------
# LIMPEZA DOS CAMPOS DE TEXTO
# ---------------------------------------------------------

# Identifica todas as colunas armazenadas como texto
colunas_texto = dados.select_dtypes(
    include=["object", "string"]
).columns

# Remove espaços extras no início e no final
# e elimina quebras de linha internas.
for coluna in colunas_texto:
    dados[coluna] = (
        dados[coluna]
        .astype("string")
        .str.strip()
        .str.replace(r"[\r\n]+", " ", regex=True)
    )


# ---------------------------------------------------------
# CRIAÇÃO DE IDENTIFICADORES COMPACTOS
# ---------------------------------------------------------

# Cria um identificador numérico para cada instituição,
# utilizando o CNPJ original como referência.
dados["id_instituicao"] = (
    pd.factorize(
        dados["cnpj_instituicao"],
        sort=True
    )[0] + 1
)

# Cria um identificador numérico para cada fornecedor,
# utilizando o CNPJ original como referência.
dados["id_fornecedor"] = (
    pd.factorize(
        dados["cnpj_fornecedor"],
        sort=True
    )[0] + 1
)

# Cria um identificador numérico para cada fabricante.
dados["id_fabricante"] = (
    pd.factorize(
        dados["no_fabricante"],
        sort=True
    )[0] + 1
)


# ---------------------------------------------------------
# CRIAÇÃO DE RÓTULOS COMPACTOS PARA O DASHBOARD
# ---------------------------------------------------------

# Cria um rótulo compacto para as instituições.
# O identificador preserva a distinção entre instituições,
# enquanto o nome abreviado mantém o dashboard legível.
dados["instituicao"] = (
    dados["id_instituicao"].astype("string")
    + " - "
    + dados["no_instituicao"]
        .fillna("Não informado")
        .str.slice(0, 50)
)

# Cria um rótulo compacto para os fornecedores.
dados["fornecedor"] = (
    dados["id_fornecedor"].astype("string")
    + " - "
    + dados["no_fornecedor"]
        .fillna("Não informado")
        .str.slice(0, 50)
)

# Cria um rótulo compacto para os fabricantes.
dados["fabricante"] = (
    dados["id_fabricante"].astype("string")
    + " - "
    + dados["no_fabricante"]
        .fillna("Não informado")
        .str.slice(0, 50)
)

# Cria um rótulo compacto para os produtos,
# mantendo o código CATMAT para identificação.
dados["produto"] = (
    dados["co_catmat"].fillna("SEM_CATMAT")
    + " - "
    + dados["ds_item"]
        .fillna("Sem descrição")
        .str.slice(0, 70)
)


# ---------------------------------------------------------
# SELEÇÃO FINAL DOS CAMPOS
# ---------------------------------------------------------

# Seleciona somente os campos que serão utilizados
# no dashboard do Data Studio.
colunas_dashboard = [
    "ano_compra",
    "id_instituicao",
    "instituicao",
    "sg_uf",
    "no_municipio",
    "co_catmat",
    "produto",
    "un_fornecimento",
    "id_fornecedor",
    "fornecedor",
    "fabricante",
    "modalidade",
    "qt_medicamento",
    "vl_preco_unitario",
    "vl_preco_total"
]

dados_looker = dados[colunas_dashboard].copy()


# ---------------------------------------------------------
# GERAÇÃO DO CSV
# ---------------------------------------------------------

print("\nGerando arquivo compacto para o Data Studio...")

dados_looker.to_csv(
    ARQUIVO_SAIDA,
    sep=",",
    index=False,
    encoding="utf-8"
)


# ---------------------------------------------------------
# VALIDAÇÃO DOS DADOS
# ---------------------------------------------------------

# Quantidade total de registros
quantidade_registros = len(dados_looker)

# Quantidade distinta de instituições
instituicoes = dados_looker[
    "id_instituicao"
].nunique()

# Quantidade distinta de fornecedores
fornecedores = dados_looker[
    "id_fornecedor"
].nunique()

# Soma do valor total registrado
valor_total = dados_looker[
    "vl_preco_total"
].sum()

# Soma da quantidade total adquirida
quantidade_total = dados_looker[
    "qt_medicamento"
].sum()


# ---------------------------------------------------------
# VALIDAÇÃO DO TAMANHO DO ARQUIVO
# ---------------------------------------------------------

# Obtém o tamanho real do arquivo em bytes
tamanho_bytes = ARQUIVO_SAIDA.stat().st_size

# Converte o tamanho para MB utilizando base decimal,
# compatível com a referência exibida pelo Data Studio.
tamanho_mb = (
    tamanho_bytes
    / 1_000_000
)

# Limite de upload do conjunto de dados:
# 100 MB em base decimal.
limite_upload_bytes = 100_000_000


# ---------------------------------------------------------
# EXIBIÇÃO DOS RESULTADOS
# ---------------------------------------------------------

print(f"\n{'=' * 70}")
print("VALIDAÇÃO DO ARQUIVO PARA O DATA STUDIO")
print(f"{'=' * 70}")

print(
    f"Quantidade de registros: "
    f"{quantidade_registros:,}"
)

print(
    f"Instituições distintas: "
    f"{instituicoes:,}"
)

print(
    f"Fornecedores distintos: "
    f"{fornecedores:,}"
)

print(
    f"Valor total: "
    f"R$ {valor_total:,.2f}"
)

print(
    f"Quantidade total: "
    f"{quantidade_total:,.0f}"
)

print(
    f"Tamanho do arquivo: "
    f"{tamanho_mb:.2f} MB"
)


# ---------------------------------------------------------
# CONFERÊNCIA DOS PRINCIPAIS INDICADORES
# ---------------------------------------------------------

# Confere se os principais resultados continuam iguais
# aos valores calculados na base consolidada original.
if (
    quantidade_registros == 367003
    and instituicoes == 854
    and fornecedores == 3663
):
    print("Validação dos dados: OK")
else:
    print("Validação dos dados: ERRO")


# ---------------------------------------------------------
# CONFERÊNCIA DO LIMITE DE UPLOAD
# ---------------------------------------------------------

# Verifica se o arquivo está abaixo do limite
# de 100 MB do Data Studio.
if tamanho_bytes < limite_upload_bytes:
    print("Tamanho para upload: OK")
else:
    print(
        "ATENÇÃO: o arquivo ultrapassa "
        "o limite de 100 MB do Data Studio."
    )


print(
    f"\nArquivo gerado em: "
    f"{ARQUIVO_SAIDA}"
)