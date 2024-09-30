import streamlit as st
import pandas as pd
import plotly.express as px 
import openai
import os

# Función para cargar los datos
@st.cache_data
def load_data():
    
    data = pd.read_csv("datos_proyecto.csv")
    return pd.DataFrame(data)

# Cargar los datos
df = load_data()

# Calcular ratios
df['Ratio de Liquidez'] = df['Current_Assets'] / df['Current_Liabilities']
df['Ratio de Deuda a Patrimonio'] = (df['Short_Term_Debt']+df["Long_Term_Debt"]) / df['Equity']
df['Cobertura de Gastos Financieros'] = df['Total_Revenue'] / df['Financial_Expenses']

# Título del dashboard
st.title('Dashboard Financiero')

# Selector de empresas
empresas = st.multiselect('Selecciona las empresas', df['Company_ID'].unique(), default=df['Company_ID'].unique())

# Filtrar datos
df_filtered = df[df['Company_ID'].isin(empresas)]

# Visualizaciones
st.header('Ratios Financieros')

# Ratio de Liquidez
fig_liquidez = px.bar(df_filtered, x='Company_ID', y='Ratio de Liquidez', title='Ratio de Liquidez')
st.plotly_chart(fig_liquidez)

# Ratio de Deuda a Patrimonio
fig_deuda = px.bar(df_filtered, x='Company_ID', y='Ratio de Deuda a Patrimonio', title='Ratio de Deuda a Patrimonio')
st.plotly_chart(fig_deuda)

# Cobertura de Gastos Financieros
fig_cobertura = px.bar(df_filtered, x='Company_ID', y='Cobertura de Gastos Financieros', title='Cobertura de Gastos Financieros')
st.plotly_chart(fig_cobertura)

# Tabla de ratios
st.header('Tabla de Ratios')
st.dataframe(df_filtered[['Company_ID', 'Ratio de Liquidez', 'Ratio de Deuda a Patrimonio', 'Cobertura de Gastos Financieros']])

# Análisis comparativo
st.header('Análisis Comparativo')
ratio_seleccionado = st.selectbox('Selecciona un ratio para comparar', ['Ratio de Liquidez', 'Ratio de Deuda a Patrimonio', 'Cobertura de Gastos Financieros'])

fig_comparativo = px.line(df_filtered, x='Company_ID', y=ratio_seleccionado, title=f'Comparación de {ratio_seleccionado}')
st.plotly_chart(fig_comparativo)

# Conclusiones y recomendaciones
st.header('Conclusiones y Recomendaciones')
st.write("""
Este dashboard permite analizar y comparar los ratios financieros clave de diferentes empresas:

1. **Ratio de Liquidez**: Un valor mayor a 1 indica que la empresa puede cubrir sus pasivos a corto plazo.
2. **Ratio de Deuda a Patrimonio**: Un valor menor indica un menor riesgo financiero.
3. **Cobertura de Gastos Financieros**: Un valor mayor indica una mejor capacidad para cubrir los gastos financieros con los ingresos.

Recomendaciones:
- Analiza la tendencia de estos ratios a lo largo del tiempo.
- Compara los ratios con los promedios del sector.
- Considera otros factores económicos y del mercado al tomar decisiones basadas en estos ratios.
""")

