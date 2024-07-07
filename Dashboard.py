#from canvasxpress.canvas import CanvasXpress
import os
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st
import time
from sklearn.datasets import load_iris

st.set_page_config(page_title="  Analysis!!!", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: Analyze Your Data")

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    # Load Iris dataset from sklearn
    iris = load_iris()
    # Create a DataFrame
    iris_df1=px.data.iris()
    iris_df = pd.DataFrame(iris_df1)
    #iris_df['target'] = iris.target
   # Display the first few rows of the DataFrame
    print(iris_df.head())
    print(iris_df.columns)
#DataEngineer
iris_df_Def=iris_df.copy().drop('species_id',axis=1)
print(iris_df_Def.head())
iris_df_Def['spatial_area']=iris_df_Def['sepal_length']*iris_df_Def['sepal_width']
iris_df_Def['petal_area']=iris_df_Def['petal_length']*iris_df_Def['petal_width']
iris_df_Def['sepal_to_petal_length_ratio'] = iris_df_Def['sepal_length'] / iris_df_Def['petal_length']
iris_df_Def['sepal_to_petal_width_ratio'] = iris_df_Def['sepal_width'] / iris_df_Def['petal_width']
print(iris_df_Def.head())
median_data=iris_df_Def.median(numeric_only=True)
print(median_data)
#build Dashboard
#Assign values to sidebars
st.sidebar.header("Choose Type of Analysis")
analysis_mode = st.sidebar.radio("Select Analysis Mode", ('IND', 'NOT','Species'))
#add_sidebar = st.sidebar.selectbox("Select Attribute",options=iris_df_Def.columns)

if analysis_mode=='IND':
    add_sidebar = st.sidebar.selectbox("Select Attribute", options=['sepal_length', 'sepal_width', 'petal_length','petal_width'
        ,'sepal_to_petal_width_ratio','sepal_to_petal_length_ratio',])
    if ((add_sidebar == 'sepal_length') | (add_sidebar == 'sepal_width') | (add_sidebar == 'petal_width') |
            (add_sidebar == 'petal_length')):
        st.markdown('## Individual Analysis')
        col1, col2, col3, col4 = st.columns(4)
        columns = [col1, col2, col3, col4]
        st.metric('Median of Sepal length', median_data['sepal_length'], 5)
        st.metric('Median of Sepal Width (cm) ', median_data['sepal_width'], 4)
        st.metric('Median of Petal length (cm) ', median_data['petal_length'], 5)
        st.metric('Median of Sepal Width(cm) ', median_data['sepal_width'], 2)
        iris_final = iris_df_Def[[col for col in iris_df_Def.columns if
                                  (col == add_sidebar) or col in ['sepal_length', 'sepal_width', 'petal_length',
                                                                  'petal_width']]]
        st.dataframe(iris_final)
        fig = px.histogram(iris_final)
        st.plotly_chart(fig, use_container_width=True)
        fig1 = px.histogram(iris_final.melt(var_name='feature', value_name='value'), x='feature', y='value')
        st.plotly_chart(fig1, use_container_width=True)
    if (add_sidebar == 'sepal_to_petal_length_ratio') | (add_sidebar == 'sepal_to_petal_width_ratio '):
        st.markdown('## Individual Analysis')
        st.metric('sepal_to_petal_length_ratio', median_data['sepal_to_petal_length_ratio'], 3)
        st.metric('sepal_to_petal_width_ratio', median_data['sepal_to_petal_width_ratio'], 2)
        iris_final = iris_df_Def[[col for col in iris_df_Def.columns if
                                  (col == add_sidebar) or col in ['sepal_to_petal_width_ratio',
                                                                  'sepal_to_petal_length_ratio', ]]]
        st.dataframe(iris_final)
        st.line_chart(iris_final)
        # c = alt.Chart(iris_final).mark_circle().encode(
        #   x='sepal_to_petal_width_ratio', y='sepal_to_petal_width_ratio')
        # st.write(c)
elif analysis_mode=='NOT':
    add_sidebar = st.sidebar.selectbox("Select Attribute", options=['spatial_area','petal_area'])
    if (add_sidebar == 'spatial_area') | (add_sidebar == 'petal_area'):
        st.markdown('## Not Individual Analysis')
        st.metric('Median of Sepal Areas', median_data['spatial_area'], 20)
        st.metric('Median of Petal Areas', median_data['petal_area'], 10)
        iris_final = iris_df_Def[[col for col in iris_df_Def.columns if
                                  (col == add_sidebar) or col in ['petal_area', 'spatial_area', ]]]
        st.dataframe(iris_final)
        # Create donut chart
        fig = go.Figure(data=[go.Pie(labels=iris_final.columns, values=iris_final.mean(), hole=.3)])

        # Display donut chart in Streamlit
        st.markdown('## Donut Chart of Mean Values')
        st.plotly_chart(fig)
else:
    st.markdown('## Species Analysis')
    fig = px.scatter(
        iris_df_Def,
        x="sepal_width",
        y="sepal_length",
        color="species",
        size="petal_length",
        hover_data=["petal_width"] )
    st.plotly_chart(fig, key="iris", on_select="rerun")




