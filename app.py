# app.py
import streamlit as st
from log_processor import analyze_logs_with_ollama
from prompts import build_prompt
import os

st.set_page_config(page_title="Анализатор логов", layout="wide")
st.title("Анализатор логов безопасности")

# Секция для ввода
st.subheader("Укажите путь к логам или вставьте их содержимое")
log_source = st.radio("Выберите источник данных:", ["Путь к файлу", "Ввести текст"])

if log_source == "Путь к файлу":
    path = st.text_input("Введите путь к файлу логов:")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            logs = f.read()
    else:
        logs = ""
        st.warning("Файл не найден.")
else:
    logs = st.text_area("Вставьте содержимое логов сюда:")

user_prompt = st.text_area("Дополнительные указания (необязательно):")

# Настройки модели
st.sidebar.header("Настройки модели")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.9)
top_k = st.sidebar.slider("Top-k", 1, 100, 40)
max_tokens = st.sidebar.slider("Max Tokens", 100, 128000, 40000)

options = {
    "temperature": temperature,
    "top_p": top_p,
    "top_k": top_k,
    "num_predict": max_tokens
}

if st.button("Выполнить анализ"):
    if not logs.strip():
        st.error("Логи не могут быть пустыми.")
    else:
        full_prompt = build_prompt(logs, user_prompt)
        with st.spinner("Модель анализирует логи..."):
            result = analyze_logs_with_ollama(full_prompt, options=options)
        st.markdown("Результат анализа:")
        st.markdown(result)