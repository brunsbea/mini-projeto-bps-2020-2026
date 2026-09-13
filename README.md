# Mini-Projeto BPS 2020–2026

Mini-projeto de análise de dados do Banco de Preços em Saúde (BPS), desenvolvido no Módulo 2 de Visualização de Dados e Business Intelligence.

## 1. Objetivo do projeto

O objetivo deste projeto é desenvolver uma solução de análise e visualização de dados para acompanhar as compras de medicamentos e dispositivos médicos registradas no Banco de Preços em Saúde (BPS) entre os anos de 2020 e 2026.

A análise busca transformar os dados públicos do BPS em informações que auxiliem na compreensão da evolução das compras, dos valores registrados, das instituições compradoras, dos fornecedores, dos produtos adquiridos e das diferenças de preços encontradas no período.

## 2. Contextualização do problema

A aquisição de medicamentos, materiais hospitalares e dispositivos médicos envolve grande volume de recursos, diferentes instituições, fornecedores, fabricantes e modalidades de compra.

Nesse contexto, a análise dos dados do BPS permite acompanhar os valores registrados, identificar os produtos mais adquiridos, analisar a distribuição das compras entre estados e municípios e investigar diferenças de preços entre transações comparáveis.

As diferenças de preços encontradas não devem ser interpretadas automaticamente como economia, sobrepreço ou irregularidade, pois podem estar relacionadas a fatores como fabricante, apresentação, unidade de fornecimento, quantidade, localidade, modalidade de compra, período e características da negociação.

## 3. Fonte dos dados

Os dados utilizados são provenientes do Banco de Preços em Saúde (BPS), disponibilizado pelo Ministério da Saúde no Portal Brasileiro de Dados Abertos.

Foram utilizadas as bases anuais referentes aos anos de:

2020, 2021, 2022, 2023, 2024, 2025 e 2026.

Também foi consultado o dicionário de dados oficial do BPS para compreensão e validação dos principais campos utilizados na análise.

## 4. Procedimentos para download e concatenação das bases

Os arquivos anuais em formato CSV foram baixados individualmente e armazenados na pasta:

`data/raw/`

Os arquivos foram organizados com os seguintes nomes:

`BPS_2020.csv` até `BPS_2026.csv`.

Durante a análise inicial foi identificado que todos os arquivos possuem 36 colunas, com os mesmos nomes e na mesma ordem. Os arquivos utilizam ponto e vírgula (`;`) como separador.

A consolidação foi realizada em Python com a biblioteca pandas. Cada arquivo anual foi processado individualmente e seus registros foram adicionados ao arquivo consolidado, evitando a necessidade de manter todas as bases simultaneamente na memória.

A base final foi gerada em:

`data/processed/BPS_20_26_BeatrizBruns.csv`

O conjunto consolidado possui 367.003 registros referentes aos anos de 2020 a 2026.

## 5. Tratamentos e transformações realizados

Antes da consolidação, foram realizadas verificações de estrutura, tipos de dados, valores nulos, duplicidades, formatos e inconsistências lógicas.

Foram realizados os seguintes tratamentos:

- validação da estrutura das bases anuais;
- confirmação do encoding UTF-8;
- remoção de espaços extras no início e no final dos campos de texto;
- conversão dos campos `dt_compra` e `dt_insercao` para formato de data;
- tratamento dos campos de CNPJ e outros identificadores como texto;
- conversão e validação dos campos quantitativos e financeiros;
- preservação dos valores nulos quando não havia informação confiável para substituí-los;
- verificação de registros completamente duplicados;
- validação da relação entre quantidade, preço unitário e preço total;
- validação da correspondência entre `ano_compra` e o ano presente em `dt_compra`;
- verificação de quantidades e preços menores ou iguais a zero.

Não foram identificados registros completamente duplicados.

Também não foram encontrados valores inválidos nos principais campos numéricos, datas inválidas, quantidades não positivas ou preços não positivos.

A validação do preço total não apresentou divergências superiores a R$ 0,01 em relação ao cálculo:

`quantidade comprada × preço unitário`.

Algumas colunas apresentam quantidade significativa de valores nulos. Esses valores foram preservados, pois o preenchimento artificial poderia alterar o significado original dos dados.

## 6. Principais colunas utilizadas

Entre as principais colunas disponíveis na base estão:

| Campo | Descrição |
|---|---|
| `ano_compra` | Ano da compra |
| `dt_compra` | Data da compra |
| `no_instituicao` | Instituição compradora |
| `cnpj_instituicao` | CNPJ da instituição |
| `sg_uf` | Unidade Federativa |
| `no_municipio` | Município |
| `co_catmat` | Código do item no CATMAT |
| `ds_item` | Descrição do item |
| `no_fornecedor` | Nome do fornecedor |
| `no_fabricante` | Nome do fabricante |
| `qt_medicamento` | Quantidade adquirida |
| `modalidade` | Modalidade da compra |
| `vl_preco_unitario` | Preço unitário |
| `vl_preco_total` | Valor total registrado |

## 7. KPIs e métricas

Esta seção será desenvolvida na Sprint 3.

## 8. Dashboard

Esta seção será atualizada após a construção do dashboard.

## 9. Principais análises e descobertas

Esta seção será preenchida após a análise dos resultados.

## 10. Recomendações

Esta seção será preenchida após a análise dos resultados.

## 11. Limitações

Esta seção será atualizada ao final da análise considerando as limitações identificadas na base e no projeto.

## 12. Instruções para reprodução do projeto

Esta seção será finalizada após a conclusão dos scripts e da estrutura do projeto.# mini-projeto-bps-2020-2026
Mini-projeto de análise de dados do Banco de Preços em Saúde (BPS) 2020–2026.
