# Sprint 1 - Diagnóstico e Entendimento dos Dados

## 1. Bases analisadas

Foram analisadas as bases anuais do Banco de Preços em Saúde (BPS) referentes aos anos de 2020 a 2026.

Os arquivos utilizados foram:

- BPS_2020.csv
- BPS_2021.csv
- BPS_2022.csv
- BPS_2023.csv
- BPS_2024.csv
- BPS_2025.csv
- BPS_2026.csv

## 2. Estrutura das bases

A comparação automática das sete bases identificou:

- 36 colunas em cada arquivo;
- mesmos nomes de colunas em todos os anos;
- mesma ordem das colunas em todos os anos;
- utilização do ponto e vírgula (`;`) como separador.

Resultado da comparação:

> Todas as bases possuem a mesma estrutura entre 2020 e 2026.

Dessa forma, não foi necessário alterar os nomes ou a ordem das colunas antes da consolidação.

## 3. Principais campos identificados

Entre as principais colunas disponíveis nas bases estão:

- `ano_compra`: ano da compra;
- `sg_uf`: unidade federativa;
- `no_municipio`: município;
- `no_instituicao`: instituição compradora;
- `ds_item`: descrição do item;
- `no_fornecedor`: fornecedor;
- `no_fabricante`: fabricante;
- `qt_medicamento`: quantidade;
- `modalidade`: modalidade de compra;
- `vl_preco_unitario`: preço unitário;
- `vl_preco_total`: preço total.

## 4. Consulta ao dicionário de dados oficial

Foi consultado o dicionário de dados oficial do Banco de Preços em Saúde (BPS), disponibilizado pelo Ministério da Saúde e atualizado em abril de 2026.

O documento apresenta a descrição das colunas das planilhas do BPS referentes ao período de 2020 a 2026 e foi utilizado para confirmar o significado dos principais campos presentes nas bases.

A correspondência entre alguns campos utilizados no arquivo CSV e suas definições oficiais é apresentada a seguir:

| Campo na base | Definição |
|---|---|
| `ano_compra` | Ano da compra informada pela instituição compradora |
| `no_instituicao` | Nome da instituição responsável pela compra |
| `cnpj_instituicao` | CNPJ da instituição compradora |
| `no_municipio` | Município da instituição compradora |
| `sg_uf` | Unidade Federativa da instituição compradora |
| `dt_compra` | Data da compra informada pela instituição |
| `dt_insercao` | Data de inserção das informações no BPS |
| `co_catmat` | Código BR/CATMAT utilizado para identificação padronizada do item |
| `ds_item` | Descrição do item conforme o CATMAT |
| `fg_generico` | Identificação de medicamento genérico |
| `registro_anvisa` | Registro do produto na Anvisa |
| `modalidade` | Modalidade utilizada para aquisição do item |
| `tp_compra` | Classificação ou tipo da compra |
| `cnpj_fornecedor` | CNPJ da empresa fornecedora |
| `no_fornecedor` | Nome do fornecedor |
| `cnpj_fabricante` | CNPJ do fabricante |
| `no_fabricante` | Nome do fabricante |
| `qt_medicamento` | Quantidade do item adquirida na transação |
| `vl_preco_unitario` | Preço pago por unidade do item adquirido |
| `vl_preco_total` | Valor total da aquisição do item, correspondente ao preço unitário multiplicado pela quantidade adquirida |

A consulta ao dicionário também será utilizada como referência durante as etapas de tratamento dos dados, definição das métricas e interpretação dos resultados.

## 5. Características identificadas nos dados

Na análise inicial, foram observadas as seguintes características:

- As colunas `dt_compra` e `dt_insercao` foram identificadas como texto e precisarão ser tratadas como datas na etapa de preparação dos dados.
- As colunas de valores financeiros `vl_preco_unitario`, `vl_preco_total` e `vl_capacidade` foram identificadas como numéricas.
- A coluna `qt_medicamento` foi identificada como numérica inteira.
- As colunas de CNPJ foram identificadas como numéricas e deverão ser avaliadas como identificadores durante o tratamento dos dados.
- Foram identificados valores nulos em algumas colunas, como `fg_generico`, `sg_unidade_medida`, `registro_anvisa`, `vl_capacidade`, `nu_ata` e `ds_observacao`.
- Também foram observados valores nulos em algumas ocorrências de `dt_insercao` e `no_instituicao`.

Os valores nulos não serão removidos automaticamente. O tratamento será definido na etapa de preparação e consolidação das bases.

## 6. Perguntas de negócio

O dashboard deverá buscar responder às seguintes perguntas:

1. Como evoluiu o valor total das compras e a quantidade adquirida entre 2020 e 2026?

2. Quais estados, municípios e instituições concentram o maior volume financeiro de compras?

3. Quais medicamentos e dispositivos apresentam os maiores volumes de compras, considerando valor total e quantidade?

4. Quais fornecedores e fabricantes possuem maior participação nas compras registradas?

5. Como os preços unitários variam entre produtos comparáveis ao longo do período e entre diferentes compradores ou fornecedores?

6. Quais modalidades de compra são mais utilizadas e qual o impacto financeiro de cada uma?

## 7. Próxima etapa

Na Sprint 2 será realizada a preparação e consolidação das bases anuais, incluindo:

- padronização das colunas;
- verificação e correção dos tipos de dados;
- tratamento das datas;
- tratamento de quantidades e valores monetários;
- verificação de valores nulos e inconsistências;
- avaliação de duplicidades;
- concatenação das bases de 2020 a 2026;
- preservação do identificador do ano da compra.