import streamlit as st
import rasterio
import numpy as np
import pandas as pd
import plotly.express as px

st.title("Análise Espectral: Turbidez e Oxigênio Dissolvido")

# Upload da imagem TIFF
uploaded_file = st.file_uploader("Faça o upload de uma imagem TIFF", type=["tif", "tiff"])

if uploaded_file is not None:
    with rasterio.open(uploaded_file) as src:

        # Verificar se há pelo menos 3 bandas
        if src.count < 3:
            st.error("A imagem precisa ter pelo menos 3 bandas para realizar a análise.")
        else:
            # Selecionar bandas para os cálculos
            bandas = list(range(1, src.count + 1))
            banda_red = st.selectbox("Selecione a banda do Vermelho (Red):", bandas)
            banda_nir = st.selectbox("Selecione a banda do Infravermelho (NIR):", bandas)
            banda_green = st.selectbox("Selecione a banda do Verde (Green):", bandas)

            # Carregar as bandas selecionadas
            red = src.read(banda_red).astype(float)
            nir = src.read(banda_nir).astype(float)
            green = src.read(banda_green).astype(float)

            # Calcular índices espectrais
            turbidez = (red / green)  # Exemplo: índice baseado em Red e Green
            oxigenio_dissolvido = (nir - red) / (nir + red)  # Exemplo: NDVI adaptado

            # Amostragem para performance (opcional)
            turbidez_flat = turbidez.flatten()
            oxigenio_flat = oxigenio_dissolvido.flatten()
            sample_size = st.slider("Tamanho da amostra (pontos)", 1000, 50000, 10000)
            indices_df = pd.DataFrame({
                "Turbidez": turbidez_flat[:sample_size],
                "Oxigênio Dissolvido": oxigenio_flat[:sample_size],
            })

            # Plotar os índices espectrais
            st.subheader("Gráficos de Análise Espectral")

            # Scatter plot: Turbidez vs Oxigênio Dissolvido
            fig = px.scatter(
                indices_df,
                x="Turbidez",
                y="Oxigênio Dissolvido",
                title="Turbidez vs Oxigênio Dissolvido",
                labels={"Turbidez": "Turbidez", "Oxigênio Dissolvido": "Oxigênio Dissolvido"},
            )
            st.plotly_chart(fig)

            # Histogramas dos índices
            fig_hist = px.histogram(
                indices_df.melt(var_name="Índice", value_name="Valor"),
                x="Valor",
                color="Índice",
                title="Distribuição dos Índices",
                labels={"Valor": "Valor do Índice", "Índice": "Tipo de Índice"},
                nbins=50,
            )
            st.plotly_chart(fig_hist)
