import datetime
import time

import streamlit as st
import pandas as p
import numpy as np

st.write("This is inside the container")
st.title("This is the app title")
st.header("This is the header")
st.markdown("This is the markdown")
st.subheader("This is the subheader")
st.caption("This is the caption")
st.code("x = 2021")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')

check_box = st.checkbox('Yes')
st.write(check_box)
st.button('Click Me', on_click=st.write("button clicked"))

radio_select = st.radio('Pick your gender', ['Male', 'Female'])
st.write(radio_select)
select_box = st.selectbox('Pick a fruit', ['Apple', 'Banana', 'Orange'])
st.write(select_box)
multiple_choice = st.multiselect('Choose a planet', ['Jupiter', 'Mars', 'Neptune'])
st.write(multiple_choice)
slider = st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.write(slider)
slider_pick = st.slider('Pick a number', 0, 50, step=5)
st.write(slider_pick)

number_inp = st.number_input('Pick a number', 0, 10)
st.write(number_inp)

text_inp = st.text_input('Email address')
st.write(text_inp)
date_inp = st.date_input('Traveling date', )
st.write(date_inp)
time_inp = st.time_input('School time')
st.write(time_inp)
description_inp = st.text_area('Description')
st.write(description_inp)
uploader = st.file_uploader('Upload a photo')
st.write(type(uploader))
color = st.color_picker('Choose your favorite color')
st.write(color)

st.balloons()  # Celebration balloons
st.progress(10)  # Progress bar
with st.spinner('Wait for it...'):
    pass
    # time.sleep(5)  # Simulating a process delay

st.success("You did it!")
st.error("Error occurred")
st.warning("This is a warning")
st.info("It's easy to build a Streamlit app")
st.exception(RuntimeError("RuntimeError exception"))

st.sidebar.title("Sidebar Title")
st.sidebar.button("Click me")
st.sidebar.markdown("This is the sidebar content")

with st.container():
    st.write("This is invisible container to group widgets")

with st.container():
    array = np.random.rand(20, 2)
    dataframe = p.DataFrame(
        data=array, columns=("first", "second")
    )
    st.write(dataframe)
    st.line_chart(dataframe)

    array = np.random.rand(100, 5)
    dataframes = p.DataFrame(
        data=array, columns=("first", "second", "third", "fourth", "fifth")
    )
    st.scatter_chart(dataframes)

