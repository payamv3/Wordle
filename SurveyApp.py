import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

df = pd.read_csv('Fashion_Disability_Survey.csv')

df.drop(index=[0,1], inplace = True)
df.drop(columns = {'StartDate','EndDate','Status','Progress','Duration (in seconds)','Finished','RecordedDate','ResponseId','DistributionChannel','UserLanguage'}, inplace = True)

Q1 = df['Q1'].str.split(',', expand=True).stack().str.get_dummies().sum(level=0)
Q1 = Q1.T
Q1['Sum'] = Q1.sum(axis = 1)
Q1 = Q1[['Sum']].reset_index()

Q9 = df['Q9'].str.split(',', expand=True).stack().str.get_dummies().sum(level=0)
Q9 = Q9.T
Q9['Sum'] = Q9.sum(axis = 1)
Q9 = Q9[['Sum']].reset_index()

col1,col2 = st.columns(2)

histogram1 = alt.Chart(Q1).mark_bar(cornerRadiusTopRight=3,
    cornerRadiusBottomRight=3, size = 40).encode(
    alt.X('Sum', axis = alt.Axis(title = None, labels = False, grid = False, ticks = False, tickSize=0, labelPadding = 10)),
    alt.Y('index', axis = alt.Axis(title = None, grid = False, labelFontSize = 14, tickSize = 0, labelPadding = 10)),
    color = alt.value('gold')
).properties(width = 300, height = 300)

text1 = histogram1.mark_text(
    align='center',
    baseline='middle' , dx= 10, dy = 0
).encode(
    text='Sum'
)

histogram2 = alt.Chart(Q9).mark_bar(cornerRadiusTopRight=3,
    cornerRadiusBottomRight=3, size = 40).encode(
    alt.X('Sum', axis = alt.Axis(title = None, labels = False, grid = False, ticks = False, tickSize=0, labelPadding = 10)),
    alt.Y('index', axis = alt.Axis(title = None, grid = False, labelFontSize = 14, tickSize = 0, labelPadding = 10)),
    color = alt.value('purple')
).properties(width = 400, height = 400)

text2 = histogram2.mark_text(
    align='center',
    baseline='middle' , dx= 10, dy = 0
).encode(
    text='Sum'
)
with col1:
    st.subheader("Fashion Roles Taken on by Repondents")
    st.altair_chart(((histogram1 + text1)).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)
with col2:
    st.subheader("Why Won't You Work With a Client With Disability?")
    st.altair_chart(((histogram2 + text2)).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)