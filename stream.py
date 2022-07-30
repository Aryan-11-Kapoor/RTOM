import streamlit as st
from final_rtom import *
from badacc import *
st.image('https://miro.medium.com/max/568/1*Y1S4hciQTfrB3xJuk2remA.png')
st.title("Real Time Object Measurement App")
st.subheader("This app allows you to measure objects in real-time !!!")
st.text("We use OpenCV and Streamlit for this demo")
options = st.sidebar.radio("select",('Real','Static'))
if options == 'Real':
    try:    
        live()
    except:
        pass
elif options == 'Static':
    try:
        static()
    except:
        pass
