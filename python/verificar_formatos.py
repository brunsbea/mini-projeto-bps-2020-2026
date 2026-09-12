from pathlib import Path
import pandas as pd

# Define a pasta onde estão armazenadas as bases originais
PASTA_DADOS = Path("data/raw")

# Define os anos que serão analisados
anos = range(2020, 2027)

# Colunas que representam CNPJs e devem ser analisadas como texto
colunas_cnpj = [
    "cnpj_instituicao",
    "cnpj_fornecedor",
    "cnpj_fabricante"
]

# Colunas de data que precisarão ser convertidas
colunas_data = [
    "dt_compra",
    "dt_insercao"
]

# Colunas numéricas importantes para os cálculos do projeto
colunas_numericas = [
    "qt_medicamento",
    "vl_capacidade",
    "vl_preco_unitario",
    "vl_preco_total"
]


# Percorre cada uma das bases anuais
for ano in anos:

    arquivo = PASTA_DADOS / f"BPS_{ano}.csv"

    print(f"\n{'=' * 70}")
    print(f"VERIFICAÇÃO DE FORMATOS - {ano}")
    print(f"{'=' * 70}")

    # Lê inicialmente todos os campos como texto.
    # Isso permite verificar o conteúdo original antes das conversões.
    dados = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
        dtype="string"
    )

    # ---------------------------------------------------------
    # VERIFICAÇÃO DOS CAMPOS DE DATA
    # ---------------------------------------------------------

    print("\nDATAS:")

    for coluna in colunas_data:

        # Converte os valores para data apenas para testar a validade.
        # errors="coerce" transforma valores inválidos em NaT.
        datas_convertidas = pd.to_datetime(
            dados[coluna],
            format="mixed",
            dayfirst=True,
            errors="coerce"
        )

        # Conta somente valores preenchidos que não puderam ser convertidos
        datas_invalidas = (
            dados[coluna].notna()
            & datas_convertidas.isna()
        ).sum()

        print(f"{coluna}: {datas_invalidas:,} valor(es) inválido(s)")

        # Exibe alguns exemplos do formato original
        exemplos = dados[coluna].dropna().head(3).tolist()
        print(f"  Exemplos: {exemplos}")

    # ---------------------------------------------------------
    # VERIFICAÇÃO DOS CNPJs
    # ---------------------------------------------------------

    print("\nCNPJs:")

    for coluna in colunas_cnpj:

        # Remove qualquer caractere que não seja número
        cnpj_limpo = (
            dados[coluna]
            .dropna()
            .str.replace(r"\D", "", regex=True)
        )

        # Conta quantos dígitos aparecem nos CNPJs
        tamanhos = cnpj_limpo.str.len().value_counts().sort_index()

        print(f"{coluna}:")
        print(tamanhos)

    # ---------------------------------------------------------
    # VERIFICAÇÃO DOS CAMPOS NUMÉRICOS
    # ---------------------------------------------------------

    print("\nCAMPOS NUMÉRICOS:")

    for coluna in colunas_numericas:

        # Tenta converter os valores para número
        valores_convertidos = pd.to_numeric(
            dados[coluna],
            errors="coerce"
        )

        # Conta valores preenchidos que não puderam ser convertidos
        valores_invalidos = (
            dados[coluna].notna()
            & valores_convertidos.isna()
        ).sum()

        print(f"{coluna}: {valores_invalidos:,} valor(es) inválido(s)")

    # ---------------------------------------------------------
    # VALIDAÇÃO DO PREÇO TOTAL
    # ---------------------------------------------------------

    print("\nVALIDAÇÃO DO PREÇO TOTAL:")

    # Converte os campos necessários para valores numéricos
    quantidade = pd.to_numeric(
        dados["qt_medicamento"],
        errors="coerce"
    )

    preco_unitario = pd.to_numeric(
        dados["vl_preco_unitario"],
        errors="coerce"
    )

    preco_total = pd.to_numeric(
        dados["vl_preco_total"],
        errors="coerce"
    )

    # Calcula o preço total esperado:
    # quantidade comprada x preço unitário
    preco_total_calculado = quantidade * preco_unitario

    # Calcula a diferença entre o valor informado na base
    # e o valor obtido pelo cálculo
    diferenca = (
        preco_total - preco_total_calculado
    ).abs()

    # Considera como divergência diferenças superiores a 1 centavo
    registros_divergentes = (diferenca > 0.01).sum()

    print(
        f"Registros com diferença superior a R$ 0,01: "
        f"{registros_divergentes:,}"
    )

    # ---------------------------------------------------------
    # VERIFICAÇÃO DE INCONSISTÊNCIAS LÓGICAS
    # ---------------------------------------------------------

    print("\nINCONSISTÊNCIAS LÓGICAS:")

    # Converte a data da compra para permitir a comparação com ano_compra
    data_compra = pd.to_datetime(
        dados["dt_compra"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # Converte o ano da compra para valor numérico
    ano_compra = pd.to_numeric(
        dados["ano_compra"],
        errors="coerce"
    )

    # Verifica se o ano informado corresponde ao ano da data da compra
    ano_inconsistente = (
        ano_compra != data_compra.dt.year
    ).sum()

    print(
        f"Ano da compra diferente da data da compra: "
        f"{ano_inconsistente:,}"
    )

    # Converte os principais campos numéricos
    quantidade = pd.to_numeric(
        dados["qt_medicamento"],
        errors="coerce"
    )

    preco_unitario = pd.to_numeric(
        dados["vl_preco_unitario"],
        errors="coerce"
    )

    preco_total = pd.to_numeric(
        dados["vl_preco_total"],
        errors="coerce"
    )

    # Verifica valores iguais ou inferiores a zero
    quantidade_nao_positiva = (quantidade <= 0).sum()
    preco_unitario_nao_positivo = (preco_unitario <= 0).sum()
    preco_total_nao_positivo = (preco_total <= 0).sum()

    print(
        f"Quantidade menor ou igual a zero: "
        f"{quantidade_nao_positiva:,}"
    )

    print(
        f"Preço unitário menor ou igual a zero: "
        f"{preco_unitario_nao_positivo:,}"
    )

    print(
        f"Preço total menor ou igual a zero: "
        f"{preco_total_nao_positivo:,}"
    )

    # Libera a base antes de carregar o próximo ano
    del dados