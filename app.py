from vector_search.vector_search import search
# Импортируем необходимые библиотеки
import streamlit as st
import pandas as pd

# Функция поиска


# Создаем интерфейс пользователя с Streamlit
st.title("Поиск похожей песни по фразе")
query = st.text_input("Введите фразу для поиска:")

if query:
    st.subheader("Результаты поиска:")
    results = search(query)
    if results:
        for result in results:
            st.markdown(
                f"**INDEX:** {result['doc_id']} | **Ссылка:** [{result['link']}]"
                f"({result['link']}) | **Косинусное сходство:** {result['cosine_sim']:.2f}")
    else:
        st.write("По вашему запросу ничего не найдено.")
