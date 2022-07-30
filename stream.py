import streamlit as st
from final_rtom import *
from badacc import *
st.image('https://miro.medium.com/max/568/1*Y1S4hciQTfrB3xJuk2remA.png')
st.title("Real Time Object Measurement App")
st.subheader("This app allows you to measure objects in real-time !!!")
st.text("We use OpenCV and Streamlit for this demo")
sideb = st.sidebar
check1 = sideb.button("Live")
check2 = sideb.button("Static")
if check1:
    try:
        live()
    except:
        pass
elif check2:
    try:
        static()
    except:
        pass