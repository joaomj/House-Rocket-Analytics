# O QUE FALTA FAZER:
# > formatar os números do mapa: 02 casas depois da vírgula, pontuação de milhar.

# IMPORTS
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import streamlit as st
import plotly.express as px

st.set_page_config(page_title = 'House Rocket Analytics', layout = 'centered')

# ====================================================
# FUNÇÕES
# ====================================================

# coleta de dados
@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data

# =========================================
# formatação dos dados
def format_data(df):

    # Elimina imóveis duplicados
    df = df.drop_duplicates(subset=['id']).copy(deep=True).reset_index(drop=True)

    # TRATAMENTO DE DATAS
    # Converte para formato YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # Converte de 'int' para 'datetime' no formato YYYY-MM-DD
    df['yr_built'] = df['yr_built'].astype(str)
    df['yr_built'] = pd.to_datetime(df['yr_built']).dt.strftime('%Y')

    df['yr_renovated'] = df['yr_renovated'].astype(str)
    df['yr_renovated'] = df['yr_renovated'].replace('0', '1900') # PREMISSA: quando não há reforma, ano da reforma é '1900'
    df['yr_renovated'] = pd.to_datetime(df['yr_renovated']).dt.strftime('%Y')

    # Converte do tipo float64 para int
    df['bathrooms'] = df['bathrooms'].astype(int)
    df['floors'] = df['floors'].astype(int)

    # Exclui colunas desnecessárias
    df = df.drop(columns=['sqft_lot15', 'sqft_living15', 'view', 'grade'])

    return df

# =========================================
# Análise descritiva:
def overview_data(df):
    st.title(':house: House Rocket Analytics :house:')

    # exibe o máximo e mínimo de cada coluna para interpretação
    num_attributes = df.select_dtypes(include=['int64', 'float64'])
    num_attributes = num_attributes.drop(columns=['id', 'zipcode', 'lat', 'long'])
    maxim = pd.DataFrame(num_attributes.apply(np.max))
    minim = pd.DataFrame(num_attributes.apply(np.min))
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))
    df1 = pd.concat([maxim, minim, media, mediana, std], axis=1).reset_index()
    df1.columns = ['ATTRIBUTES', 'MAX', 'MIN', 'AVG', 'MEDIAN', 'STD']

    st.header('01. Análise Descritiva')
    st.dataframe(df1, height=600)
    
    # Verificando se as outras características do imóvel com 33 quartos são compatíveis
    df2 = df.loc[df['bedrooms'] == df['bedrooms'].max(), ['id', 'bedrooms', 'sqft_lot', 'floors', 'sqft_above', 'sqft_basement']]
    df.loc[df['bedrooms'] == 33, 'bedrooms'] = 3 # PREMISSA: o '33' foi erro de digitação. O correto é '3'
    
    st.header('02. Procurando Outliers:')
    st.write('Existe um imóvel com 33 quartos. É um imóvel real ou foi um erro de digitação?')
    st.write('Vamos descobrir conferindo outras características desse imóvel :point_down:')
    st.write(df2)

    st.write('Muito improvável que um imóvel tenha 33 quartos em um terreno de 6000 pés quadrados.')
    st.write('Então eu vou assumir que o número 33 foi um erro de digitação. O número real de quartos é 3 :sunglasses:')

    return None

# # ====================================================
# # HIPÓTESES
# # ====================================================

def percentage_chart(df1, x_axis, percentage_param):
    # utilizando a função pct para mostrar a diferença %
    
    percentage_diff = percentage_param + ' %'
    df1[percentage_diff] = (df1[percentage_param].pct_change())*100.0
    
    fig = px.bar(df1, 
                x=x_axis, 
                y=percentage_diff,
                hover_data={percentage_diff:':.2f'})
    st.plotly_chart(fig, use_container_width=True)

    return None

# ====================================================
def hypothesis_01(df):
    # HIPÓTESE 01 - IMÓVEIS COM VISTA PARA ÁGUA SÃO 30% MAIS CAROS

    st.subheader('3.1 Imóveis com vista para a água são 30% mais caros?')
    df1 = df[['price', 'waterfront']].groupby('waterfront').median().reset_index()
    df1.columns = ['waterfront_status', 'median_price']

    percentage_chart(df1, 'waterfront_status', 'median_price')
    st.write('RESULTADO: FALSO. Imóveis c/vista para água têm preço mediano 211% maiores.')

    return None

# ====================================================
def hypothesis_02(df):
    # HIPÓTESE 02 - Imóveis construídos antes de 1955 são 50% mais baratos, em média.

    st.subheader('3.2 Imóveis construídos antes de 1955 são 50% mais baratos?')

    df1 = df[['price', 'yr_built']].copy().reset_index()
    df1.loc[df1['yr_built'] < '1955', 'yr_built_status'] = 'before_1955'
    df1.loc[df1['yr_built'] >= '1955', 'yr_built_status'] = 'after_1955'

    df2 = df1[['price', 'yr_built_status']].groupby('yr_built_status').median().reset_index()
    percentage_chart(df2, 'yr_built_status', 'price')
    st.write('RESULTADO: FALSO. O preço deles é 0.44% maior que dos imóveis construídos depois de 1955')

    return None

# ====================================================
def hypothesis_03(df):
    # HIPÓTESE 03 - Imóveis sem porão têm área total 40% maior que imóveis com porão.

    st.subheader('3.3 Imóveis sem porão têm área total 40% maior que imóveis com porão?')

    df1 = df[['sqft_lot', 'sqft_basement']].copy().reset_index()
    df1['basement'] = 'No'
    df1.loc[df1['sqft_basement'] > 0, 'basement'] = 'Yes'

    df2 = df1[['sqft_lot', 'basement']].groupby('basement', sort=False).median().reset_index()
    df2 = df2.sort_values(by='sqft_lot')
    percentage_chart(df2, 'basement', 'sqft_lot')
    #st.dataframe(df2)
    st.write('RESULTADO: FALSO. Imóveis sem porão têm área total 1.68% maior que imóveis com porão.')

    return None

# ====================================================
def hypothesis_04(df):
    # HIPÓTESE 04 - O crescimento dos preços YoY é de 10%

    st.subheader('3.4 O crescimento dos preços YoY foi de 10%?')
    df1 = df[['date', 'price']].copy().reset_index()

    df1['year'] = pd.to_datetime(df1['date']).dt.strftime('%Y')

    # agrupar por ano
    df2 = df1[['year', 'price']].groupby('year').median().reset_index()

    percentage_chart(df2, 'year', 'price')
    #st.dataframe(df2)
    st.write('RESULTADO: FALSO. Os preços aumentaram apenas 0.44% de 2014 a 2015.')

    return None

# ====================================================
def hypothesis_05(df):
    #HIPÓTESE 05 - Imóveis com 03 banheiros têm crescimento de preço MoM de 15%.
    #SUGESTÃO: obter a variação média dos preços MoM e tentar plotar.

    st.subheader('3.5 Imóveis com 03 banheiros têm crescimento de preço MoM de 15%?')
    df1 = df[['price', 'bathrooms', 'date']].copy()

    df1 = df1[df1['bathrooms'] == 3].reset_index(drop=True) # montar um df apenas com imóveis com 03 banheiros

    # cria coluna mês do ano: YYYY-mm
    df1['month_yr'] = pd.to_datetime(df1['date']).dt.strftime('%Y-%m')

    # agrupar por data
    df2 = df1[['month_yr', 'price']].groupby('month_yr').median().reset_index()

    percentage_chart(df2, 'month_yr', 'price')
    #st.dataframe(df2)
    st.write('RESULTADO: FALSO. Apenas em Out/2014 e Mar/2015 os preços desses imóveis aumentaram acima de 13%.')

    return None

# ====================================================
# PERGUNTAS DE NEGÓCIO
# ====================================================
def first_question(df):
    # 1. Quais imóveis a House Rocket deveria comprar? Por qual preço?
    st.subheader('4.1 Quais imóveis a House Rocket deveria comprar? Por qual preço?')
    df1 = df.copy()

    # Obter o preço por m2
    # m2 = sqft/10,764
    df1['price_m2'] = 0.0
    df1['price_m2'] = df1['price']*10.764
    df1['price_m2'] = df1['price_m2']/df1['sqft_lot']

    # Agrupar os imóveis por zipcode, mês do ano e condition
    # e obter o preço por m2 mediano
    df1['month'] = pd.to_datetime(df1['date']).dt.strftime('%m')
    df2 = df1[['month', 'price_m2', 'zipcode', 'condition']].groupby(['zipcode', 'month', 'condition']).median().reset_index()
    df2 = df2.rename(columns={'price_m2':'market_price_m2'})
    df3 = pd.merge(df1, df2, on=['zipcode', 'month', 'condition'], how='inner')
    
    # comparar o price_m2 com median_price_m2_by_month_and_zipcode
    # comprar aqueles com mais de 30% de desconto em relação à mediana E com condições regulares
    for i in range(len(df3)):
        if (df3.loc[i,'price_m2'] < (0.7* df3.loc[i,'market_price_m2'])) & (df3.loc[i, 'condition'] > 2):
            df3.loc[i, 'status'] = 'buy'
            df3.loc[i, 'buy_price'] = df3.loc[i, 'price']
        else:
            continue


    # exclui os imóveis não comprados
    df4 = df3[df3['status'] == 'buy'].reset_index(drop=True)
    
    st.write('A. Obtive o preço mediano do m2 ajustado por mês, condição e código postal = preço de mercado.')
    st.write('B. Comparei o preço do m2 de cada imóvel com o preço de mercado.')
    st.write('C. Recomenda COMPRA dos imóveis com preço/m2 inferior a 70% do preço de mercado E em condições razoáveis.')
    st.write('Abaixo está uma amostra dos imóveis com recomendação de COMPRA:')
    st.dataframe(df4[['id', 'condition', 'price_m2', 'market_price_m2', 'status', 'buy_price']].sample(10).style.format(subset=['price_m2', 'market_price_m2', 'buy_price'] ,formatter="{:.2f}"))

    # salva tabela em arquivo
    df4.to_csv('~/houses_bought.csv')

    return df4

# ====================================================
def second_question(df):
    # 2. Uma vez comprado, quando a House Rocket deveria vender o imóvel? Por qual preço?
    st.subheader('4.2 Uma vez comprado, quando a House Rocket deveria vender o imóvel? Por qual preço?')
    
    for i in range(len(df)):
        if (df.loc[i, 'status'] == 'buy') & (df.loc[i, 'market_price_m2'] > (2 * df.loc[i, 'price_m2'])): #(df.loc[i,'price_m2'] <= (0.5 * df.loc[i,'market_price_m2'])):
            df.loc[i, 'status'] = 'sell'
            df.loc[i, 'sell_price'] = df.loc[i,'market_price_m2'] * df.loc[i, 'sqft_lot']
        else:
            df.loc[i, 'sell_price'] = 0.0

    st.write('A. Se o preço de mercado é, pelo menos, o dobro do preço/m2 do imóvel comprado...')
    st.write('B. Recomenda VENDA para esses imóveis.')
    st.write('Abaixo está uma amostra dos imóveis com recomendação de VENDA:')
    st.dataframe(df[['id', 'condition', 'price_m2', 'market_price_m2', 'status', 'buy_price', 'sell_price']].sample(10).style.format(subset=['price_m2', 'market_price_m2', 'buy_price', 'sell_price'] ,formatter="{:.2f}"))
    
    # salva em arquivo
    df.to_csv('~/houses_sold.csv')

    return df

# ====================================================
def financial_result(df):
    # cria tabela totalizando o resultado financeiro da operação:
    # número de imóveis vendidos, custo total, faturamento total e lucro total

    st.subheader('4.3 Qual seria o resultado financeiro dessas recomendações na empresa House Rocket?')

    # agrupa os imóveis por status: 'buy' ou 'sell'
    df1 = df[['buy_price', 'status', 'sell_price']].groupby('status').sum().reset_index()

    # cria a tabela com os resultados financeiros das recomendações
    df2 = pd.DataFrame(columns=['houses_sold', 'total_cost', 'total_revenue', 'total_profit'])

    # custo total = soma do preço de compra dos imóveis marcados como buy e dos imóveis marcados como sell
    df2['total_cost'] = (df1.loc[df1['status'] == 'buy', 'buy_price'].reset_index(drop=True)) + (df1.loc[df1['status'] == 'sell', 'buy_price'].reset_index(drop=True))
    
    df2['total_revenue'] = df1.loc[df1['status'] == 'sell', 'sell_price'].reset_index(drop=True)
    df2['total_profit'] = df2['total_revenue'] - df2['total_cost']
    df2['houses_sold'] = df.loc[df['status'] == 'sell', 'status'].value_counts().reset_index(drop=True)
    df2['profit_margin_%'] = (df2['total_profit']/df2['total_revenue'])*100.0 # em porcentagem

    # plot
    st.write('Caso as recomendações fossem seguidas, este seria o resultado para a House Rocket:')
    st.dataframe(df2.style.format(formatter="{:.2f}"))

    # Salva a tabela do resultado financeiro total
    df2.to_csv('~/financial_result.csv')

# ====================================================
def house_map (df):

    st.subheader("Mapa com os imóveis adquiridos: ")
    df['profit'] = df[['sell_price', 'buy_price']].apply(lambda x: 0 if x['sell_price'] == 0 else x['sell_price'] - x['buy_price'], axis=1)
    df['discount'] = (df['market_price_m2'] - df['price_m2'])/df['market_price_m2'] 

    # plot map
    fig = px.scatter_mapbox(df,
                           lat = 'lat',
                           lon = 'long',
                           size = 'discount',
                           color = 'status' ,
                           hover_name = 'status',
                           hover_data = ['id' ,'profit', 'discount'],
                           color_continuous_scale = px.colors.cyclical.IceFire,
                           size_max = 15,
                           zoom = 10
                           )
    
    fig.update_layout(mapbox_style = 'open-street-map')
    fig.update_layout(height = 600, margin = {'r':0, 'l':0, 't':0, 'b':0})
    st.plotly_chart(fig)
    

# ====================================================
# MAIN FUNCTION
# ====================================================
if __name__ == '__main__':
    # ETL

    # EXTRACTION
    path = '~/House Sales in King County.csv'
    
    # get data
    data = get_data(path)
 
    # TRANSFORMATION
    data = format_data(data)
    
    overview_data(data)

    st.header('3. Verificando hipóteses de negócio')
    hypothesis_01(data)

    hypothesis_02(data)

    hypothesis_03(data)

    hypothesis_04(data)

    hypothesis_05(data)

    st.header('4. Respondendo às perguntas de negócio')

    houses_bought = first_question(data)

    houses_sold = second_question(houses_bought)

    financial_result(houses_sold)

    house_map(houses_sold)