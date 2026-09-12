from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------

# Pasta onde estão armazenadas as bases anuais originais
PASTA_ENTRADA = Path("data/raw")

# Pasta onde será salva a base consolidada
PASTA_SAIDA = Path("data/processed")

# Nome do arquivo consolidado solicitado no projeto
ARQUIVO_SAIDA = PASTA_SAIDA / "BPS_20_26_BeatrizBruns.csv"

# Anos que serão processados
anos = range(2020, 2027)


# ---------------------------------------------------------
# DEFINIÇÃO DOS TIPOS DE CAMPOS
# ---------------------------------------------------------

# Campos utilizados como identificadores.
# Eles serão tratados como texto, pois não representam
# valores destinados a cálculos matemáticos.
colunas_identificadoras = [
    "cnpj_instituicao",
    "cnpj_fornecedor",
    "cnpj_fabricante",
    "co_catmat",
    "co_pdm",
    "co_grupo",
    "co_classe",
    "nu_processo_compra",
    "nu_ata",
    "registro_anvisa",
    "co_seq_bps"
]

# Campos que representam datas
colunas_data = [
    "dt_compra",
    "dt_insercao"
]

# Campos numéricos utilizados nas análises e nos KPIs
colunas_numericas = [
    "qt_medicamento",
    "vl_capacidade",
    "vl_preco_unitario",
    "vl_preco_total"
]


# ---------------------------------------------------------
# PREPARAÇÃO DA PASTA DE SAÍDA
# ---------------------------------------------------------

# Cria a pasta processed caso ela ainda não exista
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

# Remove uma versão anterior do arquivo consolidado,
# caso o script já tenha sido executado anteriormente
if ARQUIVO_SAIDA.exists():
    ARQUIVO_SAIDA.unlink()


# ---------------------------------------------------------
# VARIÁVEIS DE CONTROLE
# ---------------------------------------------------------

# Guarda a estrutura da primeira base para comparação
colunas_referencia = None

# Soma a quantidade de registros processados
total_registros = 0


# ---------------------------------------------------------
# PROCESSAMENTO DAS BASES
# ---------------------------------------------------------

for indice, ano in enumerate(anos):

    arquivo = PASTA_ENTRADA / f"BPS_{ano}.csv"

    print(f"\n{'=' * 70}")
    print(f"PROCESSANDO E CONSOLIDANDO {ano}")
    print(f"{'=' * 70}")

    # Lê a base anual.
    # Os campos identificadores são carregados como texto
    # para evitar que sejam interpretados como medidas numéricas.
    dados = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
        dtype={
            coluna: "string"
            for coluna in colunas_identificadoras
        }
    )

    # -----------------------------------------------------
    # VALIDAÇÃO DA ESTRUTURA
    # -----------------------------------------------------

    # Usa o primeiro arquivo como estrutura de referência
    if colunas_referencia is None:
        colunas_referencia = list(dados.columns)

    # Interrompe o processamento caso seja encontrada
    # alguma estrutura diferente entre os anos
    elif list(dados.columns) != colunas_referencia:
        raise ValueError(
            f"A estrutura da base de {ano} é diferente "
            "da estrutura de referência."
        )


    # -----------------------------------------------------
    # PADRONIZAÇÃO DOS CAMPOS DE TEXTO
    # -----------------------------------------------------

    # Identifica todas as colunas de texto
    colunas_texto = dados.select_dtypes(
        include=["object", "string"]
    ).columns

    # Remove espaços extras no início e no final dos textos
    for coluna in colunas_texto:
        dados[coluna] = (
            dados[coluna]
            .astype("string")
            .str.strip()
        )


    # -----------------------------------------------------
    # PADRONIZAÇÃO DAS DATAS
    # -----------------------------------------------------

    for coluna in colunas_data:

        # Converte as datas do formato brasileiro
        # dd/mm/aaaa para o tipo de data do pandas
        dados[coluna] = pd.to_datetime(
            dados[coluna],
            format="%d/%m/%Y",
            errors="coerce"
        )


    # -----------------------------------------------------
    # PADRONIZAÇÃO DOS CAMPOS NUMÉRICOS
    # -----------------------------------------------------

    for coluna in colunas_numericas:

        # Garante que os campos utilizados em cálculos
        # estejam armazenados como valores numéricos
        dados[coluna] = pd.to_numeric(
            dados[coluna],
            errors="coerce"
        )


    # Garante que o ano da compra permaneça numérico
    dados["ano_compra"] = pd.to_numeric(
        dados["ano_compra"],
        errors="raise"
    ).astype("int64")


    # -----------------------------------------------------
    # GRAVAÇÃO DA BASE CONSOLIDADA
    # -----------------------------------------------------

    # Na primeira base cria o arquivo e grava o cabeçalho.
    # Nos anos seguintes acrescenta os registros ao mesmo arquivo.
    dados.to_csv(
        ARQUIVO_SAIDA,
        sep=";",
        index=False,
        encoding="utf-8",
        mode="w" if indice == 0 else "a",
        header=indice == 0,
        date_format="%Y-%m-%d"
    )

    # Atualiza a quantidade total de registros processados
    total_registros += len(dados)

    print(f"Registros processados: {len(dados):,}")

    # Libera a base anual da memória antes do próximo arquivo
    del dados


# ---------------------------------------------------------
# VALIDAÇÃO FINAL DA BASE CONSOLIDADA
# ---------------------------------------------------------

print(f"\n{'=' * 70}")
print("VALIDAÇÃO DA BASE CONSOLIDADA")
print(f"{'=' * 70}")

# Lê apenas a coluna ano_compra para conferir
# o número final de registros sem carregar novamente
# todas as 36 colunas na memória
validacao = pd.read_csv(
    ARQUIVO_SAIDA,
    sep=";",
    usecols=["ano_compra"]
)

print(f"Total processado: {total_registros:,}")
print(f"Total encontrado no arquivo final: {len(validacao):,}")

print(
    "Anos presentes na base consolidada:",
    sorted(validacao["ano_compra"].unique())
)

# Confere se a quantidade gravada é igual à processada
if len(validacao) == total_registros:
    print("Validação de registros: OK")
else:
    print("Validação de registros: ERRO")

print(f"\nArquivo gerado em: {ARQUIVO_SAIDA}")