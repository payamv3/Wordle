import streamlit as st
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import seaborn as sn
import os
import altair as alt
import requests
import csv
import sys
import time

df = pd.read_csv("Wordle.csv")
df.drop(columns = {"Unnamed: 3","Unnamed: 4","Unnamed: 5","Unnamed: 6"}, inplace = True)
df.head()

opener = df['Opening Word'].to_list()
wod = df['Word of the Day'].to_list()

opener = ''.join(opener).lower()
wod = ''.join(wod).lower()

df.loc[df['Number of Tries'] == "Lost", ['Number of Tries']] = 0
df['Number of Tries'] = df['Number of Tries'].astype('int32')

st.sidebar.header("My Journey with Wordle")
st.sidebar.markdown("""In an attempt to take control of my personally generated data, I have been documenting the way I go about guessing on Wordle.""")
st.sidebar.markdown("""A Small Project by Payam Saeedi""")


def frequency(string):
    frequencies = {}
    for char in string: 
        if char in frequencies: 
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies

def keywithmaxval(frequency):
    v=list(frequency.values())
    k=list(frequency.keys())
    return k[v.index(max(v))]

col1,col2 = st.columns(2)
col1.metric(label="Most Repeated Letter in my First Guess", value=keywithmaxval(frequency(opener)))
col2.metric(label="Most Repeated Letter in the Final Answer", value=keywithmaxval(frequency(wod)))

opener_items = frequency(opener).items()
opener_list = list(opener_items)

opener_df = pd.DataFrame(opener_list)
opener_df = opener_df.rename(columns = {0:"Letter",1:"Count"})

wod_items = frequency(wod).items()
wod_list = list(wod_items)

wod_df = pd.DataFrame(wod_list)
wod_df = wod_df.rename(columns = {0:"Letter",1:"Count"})


bars1 = alt.Chart(opener_df).mark_bar(cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3, size = 30).encode(
    alt.X('Letter:O', axis = alt.Axis(grid = False, labelAngle=0, labelFontSize=12, tickSize=0, labelPadding=10)),
    alt.Y('Count:Q', axis=alt.Axis(title='Count', labels = False, grid=False)),
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Count >= max(frequency(opener).values()),  # If the year is 1810 this test returns True,
        alt.value('gold'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(title = 'Frequency of Letters in my Opener', width = 800, height = 400)

text1 = bars1.mark_text(
    align='center',
    baseline='middle' , dy = -6
).encode(
    text='Count:Q'
)


st.altair_chart((bars1 + text1).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)



bars2 = alt.Chart(wod_df).mark_bar(cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3, size = 30).encode(
    alt.X('Letter:O', axis = alt.Axis(grid = False, labelAngle=0, labelFontSize=12, tickSize=0, labelPadding=10)),
    alt.Y('Count:Q', axis=alt.Axis(title='Count', labels = False, grid=False)),
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Count >= max(frequency(wod).values()),  # If the year is 1810 this test returns True,
        alt.value('gold'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(title = 'Frequency of Letters in Word of the Day', width = 800, height = 400)

text2 = bars2.mark_text(
    align='center',
    baseline='middle' , dy = -6
).encode(
    text='Count:Q'
)


st.altair_chart((bars2 + text2).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)
