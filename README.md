# House Rocket Analytics
Projeto educacional para obter insights de negócio para a imobiliária House Rocket (fictícia).

## 1. Sobre o Projeto
### 1.1. Problema de Negócio
A House Rocket é uma imobiliária interessada em soluções de Data Science para ajudá-la na compra e venda de imóveis.

O propósito deste projeto é obter insights através da análise de dados para que a empresa encontre as melhores oportunidades no mercado imobiliário de King County. Em outras palavras, encontrar imóveis em boas condições abaixo do preço de mercado e vendê-los com lucro.

### 1.2. Data Overview
| Attribute | Description |
| :----- | :----- |
| id | Código de identificação de cada imóvel |
| date | Data de inserção do imóvel na base |
| price | Preço pedido pelo imóvel |
| bedrooms | Número de quartos |
| bathrooms | Número de banheiros |
| sqft_living | Área construída |
| sqft_lot | Área do terreno |
| floors | Número de andares |
| waterfront | Variável binária indicando se o imóvel tem vista para o mar |
| view | Uma escala de 0 a 4 indicando a qualidade da vista do imóvel |
| condition | Uma escala de 0 a 5 indicando as condições do imóvel |
| grade | Uma escala de 1 a 13 indicando a qualidade da construção e padrão arquitetônico |
| sqft_above | Área construída acima do solo |
| sqft_basement | Área construída do porão |
| yr_built | Ano de construção do imóvel |
| yr_renovated | Ano da última reforma |
| zipcode | Código postal do imóvel |
| lat | Latitude |
| long | Longitude |
| sqft_living15 | Área construída dos 15 vizinhos mais próximos |
| sqft_lot15 | Área do terreno dos 15 vizinhos mais próximos |

[Dataset from Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)  
![kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)

### 1.3. Premissas
* Todos os imóveis da base são considerados disponíveis para compra.
* Os imóveis devem ter condição mínima igual a 3 para terem compra recomendada.
* O imóvel com 33 quartos foi considerado com erro de digitação, de forma que o número de quartos foi alterado para 3.

### 1.4. Solução

**1.4.1. Análise Descritiva:** análise de cada coluna da base de dados, obtendo uma tabela com um resumo estatístico da base de dados.

**1.4.2. Teste de Hipóteses:** descobrir insights e comunicá-los ao time de negócio.

**1.4.3. Recomendações de Compra e Venda:** elaboração de um relatório recomendando a compra e venda de imóveis que atendem as condições especificadas pelo time de negócio. O objetivo é descobrir imóveis em boas condições, precificados abaixo do preço de mercado para imóveis com mesmos código postal, condição e mês do ano.

O relatório pode ser acessado aqui: [houses_sold.csv](https://github.com/joaomj/House-Rocket-Analytics/blob/master/houses_sold.csv)

**1.4.4. Resultado Financeiro das Recomendações:** foi elaborada uma tabela contabilizando o resultado financeiro para a empresa caso as recomendações fossem seguidas.

O resultado financeiro pode ser acessado aqui: [financial_result.csv](https://github.com/joaomj/House-Rocket-Analytics/blob/master/financial_result.csv)

**1.4.5. Mapa das Recomendações:** construímos um mapa que exibe cada imóvel comprado ou vendido pela House Rocket com base nas recomendações acima obtidas. O mapa permite visualizar o desconto dos imóveis em relação ao preço de mercado, além do lucro obtido com a venda de cada imóvel.


## 2. Tecnologias Utilizadas
- Python 3.10
- Visual Studio Code 1.63
- Jupyter Notebook
- Streamlit
- Heroku Cloud


## 3. Utilização
A análise dos dados pode ser acessada pela aplicação em nuvem desenvolvida neste projeto, disponível aqui: [House Rocket App](https://house-rocket-analytics-joaomj.herokuapp.com/)  
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)


## 4. Status do Projeto
O projeto está **em progresso.** Melhorias serão implementadas nas próximas versões.


## 5. Melhorias Sugeridas
- Formatação dos números para exibir apenas 02 casas decimais.
- Filtros de imóveis por atributo para exibição no mapa.
- Adicionar o endereço detalhado de cada imóvel (logradouro, número, bairro, cidade e estado).
- Mapa de densidade de imóveis por: preço de mercado, desconto e lucro obtido.


## 6. Agradecimentos
Este projeto é um exercício do curso *Python: do zero ao Data Scientist*, ministrado pelo [Meigarom Lopes](https://www.linkedin.com/in/meigarom/).


## 7. Contato
Projeto criado por Joao Marcos Visotaky Junior

Data Scientist em formação

[Portfolio de Projetos](https://joaomj.github.io/portfolio_projetos/)
