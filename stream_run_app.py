import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных
@st.cache_data 
def load_data():
    data = pd.read_csv('clean_data.csv')
    return data

df = load_data()

# Заголовок приложения
st.title('Разведочный анализ данных')

# Фильтрация данных по возрасту
age_filter = st.slider('Выберите диапазон возраста', int(df['AGE'].min()), int(df['AGE'].max()), 
                       (int(df['AGE'].min()), int(df['AGE'].max())))
df_filtered = df[(df['AGE'] >= age_filter[0]) & (df['AGE'] <= age_filter[1])]

# Показать первые строки данных
if st.checkbox('Показать первые строки отфильтрованных данных'):
    st.write(df_filtered.head())

# Показать описательные статистики
if st.checkbox('Показать описательные статистики'):
    st.write(df_filtered.describe())

# Выбор столбца и типа графика для визуализации
numeric_columns = df_filtered.select_dtypes(['float64', 'int64']).columns
selected_column = st.selectbox('Выберите столбец для построения графика распределения', numeric_columns)
graph_type = st.selectbox('Выберите тип графика', ['Гистограмма', 'Ящик с усами'])

if graph_type == 'Гистограмма':
    sns.histplot(df_filtered[selected_column], kde=True)
elif graph_type == 'Ящик с усами':
    sns.boxplot(y=df_filtered[selected_column])
st.pyplot(plt)

# Построение матрицы корреляций
if st.checkbox('Показать матрицу корреляций'):
    corr = df_filtered.corr()
    sns.heatmap(corr, annot=True, fmt=".2f")
    st.pyplot(plt)

# Интерактивные графики зависимостей
if st.checkbox('Показать графики зависимости между переменными'):
    x_column = st.selectbox('Выберите X переменную', df_filtered.columns)
    y_column = st.selectbox('Выберите Y переменную', df_filtered.columns, index=df_filtered.columns.get_loc(x_column) + 1)
    if x_column != y_column:
        sns.scatterplot(x=df_filtered[x_column], y=df_filtered[y_column])
        st.pyplot(plt)