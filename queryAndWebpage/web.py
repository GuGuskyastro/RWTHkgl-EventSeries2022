import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import  Query as q


# 展示文本；文本直接使用Markdown语法
st.markdown("# Streamlit Example")

title = st.text_input("Insert a title you want find", "")
a = "Please search a Acronym you want"
st.write(a)



if title != "":
    result = q.outPut(title)

    for i in result:
        if i == "":
            del i
    result = q.funcOne(result)

    df = pd.DataFrame(result)
    df = df.to_html(render_links=True,escape=False)
    st.write(df,unsafe_allow_html=True)


