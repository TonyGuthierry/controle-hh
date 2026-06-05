import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Controle HH Profissional", layout="wide")

# ========================
# BANCO DE DADOS
# ========================
conn = sqlite3.connect("hh.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS hh (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    nome TEXT,
    matricula TEXT,
    pacote TEXT,
    pt TEXT,
    os TEXT,
    descricao TEXT,
    hh REAL
)
""")

conn.commit()

# ========================
# CONFIG
# ========================
st.title("📊 Controle HH Semanal - Profissional")

meta = st.sidebar.number_input("Meta diária (HH)", value=10)

# ========================
# FORMULÁRIO
# ========================
st.subheader("➕ Lançar Atividade")

with st.form("form"):
    col1, col2, col3 = st.columns(3)

    data = col1.date_input("Data", value=datetime.today())
    nome = col2.text_input("Nome")
    matricula = col3.text_input("Matrícula")

    col4, col5, col6 = st.columns(3)
    pacote = col4.text_input("Pacote", value="23")
    pt = col5.text_input("Nº PT")
    os_input = col6.text_input("Ordem de Serviço")

    descricao = st.text_input("Descrição")

    hh = st.number_input("HH", min_value=0.5, step=0.5)

    submitted = st.form_submit_button("Adicionar")

    if submitted:
        if nome == "" or matricula == "":
            st.warning("Preencha Nome e Matrícula")
        elif hh <= 0:
            st.warning("HH deve ser maior que zero")
        else:
            cursor.execute("""
                INSERT INTO hh (data, nome, matricula, pacote, pt, os, descricao, hh)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (str(data), nome, matricula, pacote, pt, os_input, descricao, hh))

            conn.commit()
            st.success("✅ Registro salvo com sucesso")

# ========================
# CARREGAR DADOS
# ========================
df = pd.read_sql("SELECT * FROM hh", conn)

if not df.empty:

    st.subheader("📋 Registros")
    st.dataframe(df, use_container_width=True)

    # ========================
    # DASHBOARD
    # ========================
    st.subheader("📊 Dashboard")

    resumo = df.groupby("data")["hh"].sum().reset_index()
    resumo["Meta"] = meta
    resumo["Atingimento (%)"] = (resumo["hh"] / meta) * 100
    resumo["Status"] = resumo["hh"].apply(
        lambda x: "✅ OK" if x >= meta else "⚠️ FALTA HH"
    )

    st.dataframe(resumo, use_container_width=True)

    # KPIs
    total = df["hh"].sum()
    media = df["hh"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Total HH", f"{total:.1f}")
    col2.metric("Média HH", f"{media:.1f}")

    # ========================
    # EXPORTAR
    # ========================
    st.download_button(
        "📥 Baixar Excel",
        df.to_csv(index=False),
        file_name="controle_hh_profissional.csv"
    )

    # ========================
    # FILTRO POR FUNCIONÁRIO
    # ========================
    st.subheader("👷 Por Funcionário")

    funcionarios = df["nome"].unique()
    escolhido = st.selectbox("Selecionar", funcionarios)

    df_func = df[df["nome"] == escolhido]
    st.dataframe(df_func)

else:
    st.info("Nenhum registro ainda.")
