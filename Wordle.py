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
df["Common Letters"] = df.apply(
    lambda x: len(set(x["Opening Word"]).intersection(set(x["Word of the Day"]))),
    axis=1)
#df.drop(columns = {"Unnamed: 3","Unnamed: 4","Unnamed: 5","Unnamed: 6"}, inplace = True)

def correct_guesses(string1,string2):
    count = 0
    string1 = list(string1)
    string2 = list(string2)
    #return string1,string2
    for index in range(0,5):
        if string1[index] == string2[index]:
            count +=1
    return count

df['Correct Guesses'] = df.apply(lambda x: correct_guesses(x["Opening Word"],x["Word of the Day"]) , axis = 1)

opener = df['Opening Word'].to_list()
wod = df['Word of the Day'].to_list()

opener = ''.join(opener).lower()
wod = ''.join(wod).lower()

df.loc[df['Number of Tries'] == "Lost", ['Number of Tries']] = 0
df['Number of Tries'] = df['Number of Tries'].astype('int8')

st.sidebar.header("My Journey with Wordle")
st.sidebar.markdown("""In an attempt to take control of my personally generated data, I have been documenting the way I go about guessing on Wordle.""")
st.sidebar.markdown("""A small project by Payam Saeedi""")


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
col1.metric(label="The number of guesses it usually takes me", value=df['Number of Tries'].mean().round())
col2.metric(label="Most Repeated Letter in the Final Answer", value=keywithmaxval(frequency(wod)))

opener_items = frequency(opener).items()
opener_list = list(opener_items)

opener_df = pd.DataFrame(opener_list)
opener_df = opener_df.rename(columns = {0:"Letter",1:"Count"}).sort_values(by = 'Count', ascending = False).head()

wod_items = frequency(wod).items()
wod_list = list(wod_items)

wod_df = pd.DataFrame(wod_list)
wod_df = wod_df.rename(columns = {0:"Letter",1:"Count"}).sort_values(by = 'Count', ascending = False).head()


bars1 = alt.Chart(opener_df).mark_bar(cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3, size = 40).encode(
    alt.X('Letter:O', axis = alt.Axis(grid = False, labelAngle=0, labelFontSize=14, tickSize=0, labelPadding=10)),
    alt.Y('Count:Q', axis=alt.Axis(title='Count', labels = False, grid=False, tickSize = 0)),
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Count >= max(frequency(opener).values()),  # If the year is 1810 this test returns True,
        alt.value('gold'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(title = 'Top 5 Letters in my Opener', width = 300, height = 400)

text1 = bars1.mark_text(
    align='center',
    baseline='middle' , dy = -6
).encode(
    text='Count:Q'
)


#st.altair_chart((bars1 + text1).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)



bars2 = alt.Chart(wod_df).mark_bar(cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3, size = 40).encode(
    alt.X('Letter:O', axis = alt.Axis(grid = False, labelAngle=0, labelFontSize=12, tickSize=0, labelPadding=10)),
    alt.Y('Count:Q', axis=alt.Axis(title='Count', labels = False, grid=False, tickSize = 0)),
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Count >= max(frequency(wod).values()),  # If the year is 1810 this test returns True,
        alt.value('gold'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(title = 'Top 5 Letters in Word of the Day', width = 300, height = 400)

text2 = bars2.mark_text(
    align='center',
    baseline='middle' , dy = -6
).encode(
    text='Count:Q'
)


#st.altair_chart((bars2 + text2).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)
st.altair_chart(((bars1 + text1) | (bars2 + text2)).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)


heatmap = alt.Chart(df).mark_rect().encode(
    alt.X('Number of Tries:O',axis = alt.Axis(grid = False,  labelAngle=0, labelFontSize=14, tickSize=0, labelPadding=10)),
    alt.Y('Correct Guesses:O',axis=alt.Axis(title='Correct Guesses on The First Try',grid = False, labelAngle=0, labelFontSize=14, tickSize=0, labelPadding=10)),
    alt.Color('count():Q', scale=alt.Scale(scheme='darkgold'), legend = None)).properties(title = 'Correlation Between How Many Words I Get Right The First Time and The Number of Tries', width = 300, height = 400)

st.altair_chart((heatmap).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)


histogram1 = alt.Chart(df).mark_bar(cornerRadiusTopRight=3,cornerRadiusBottomRight=3,size = 40).encode(
    alt.X('count():Q', axis = alt.Axis(title = None, labels = False, grid = False, tickSize=0, labelPadding = 10)),
    alt.Y('Common Letters:O', axis = alt.Axis(title = None, grid = False, labelFontSize = 14, tickSize = 0, labelPadding = 10)),
    color = alt.value('gold')
).properties(title = 'How many letters did my first guess have in common with the word of the day?',width = 300, height = 200)

text3 = histogram1.mark_text(
    align='center',
    baseline='middle' , dx= 10, dy = 0
).encode(
    text='count():Q'
)

histogram2 = alt.Chart(df).mark_bar(cornerRadiusTopRight=3,cornerRadiusBottomRight=3,size = 40).encode(
    alt.X('count():Q', axis = alt.Axis(title = None, labels = False, grid = False, tickSize=0, labelPadding = 10)),
    alt.Y('Correct Guesses:O', axis = alt.Axis(title = None, grid = False, labelFontSize = 14, tickSize = 0, labelPadding = 10)),
    color = alt.value('gold')
).properties(title = 'How many letters did I get right in my first guess?',width = 300, height = 200)


text4 = histogram2.mark_text(
    align='center',
    baseline='middle' , dx= 10, dy = 0
).encode(
    text='count():Q'
)


st.altair_chart(((histogram1 + text3) | (histogram2 + text4)).configure_view(stroke = 'transparent', strokeOpacity = 0), use_container_width = True)