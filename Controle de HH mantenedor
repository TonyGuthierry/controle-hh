import streamlit as st
import pandas as pd

st.set_page_config(page_title="Controle HH", layout="wide")

st.title("📊 Controle HH Semanal")

meta = st.sidebar.number_input("Meta diária (HH)", value=10)

if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=[
        "Data", "Pacote", "PT", "OS", "Descrição", "HH"
    ])

st.subheader("➕ Lançar Atividade")

with st.form("form"):
    col1, col2, col3 = st.columns(3)
    
    data = col1.date_input("Data")
    pacote = col2.text_input("Pacote", value="23")
    pt = col3.text_input("Nº PT")

    col4, col5 = st.columns(2)
    os = col4.text_input("Ordem de Serviço")
    descricao = col5.text_input("Descrição")

    hh = st.number_input("HH", min_value=0.0, step=0.5)

    if st.form_submit_button("Adicionar"):
        nova = pd.DataFrame([{
            "Data": data,
            "Pacote": pacote,
            "PT": pt,
            "OS": os,
            "Descrição": descricao,
            "HH": hh
        }])

        st.session_state.dados = pd.concat(
            [st.session_state.dados, nova],
            ignore_index=True
        )

df = st.session_state.dados

if not df.empty:
    st.subheader("📋 Registros")
    st.dataframe(df, use_container_width=True)

    resumo = df.groupby("Data")["HH"].sum().reset_index()
    resumo["Meta"] = meta
    resumo["Status"] = resumo["HH"].apply(
        lambda x: "✅ OK" if x >= meta else "⚠️ FALTA HH"
    )

    st.subheader("📅 Resumo")
    st.dataframe(resumo, use_container_width=True)

    total = df["HH"].sum()
    st.metric("Total HH", f"{total:.1f}")
