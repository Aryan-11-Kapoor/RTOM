import numpy as np
import cv2
import streamlit as st
from PIL import Image
import imutils
import scipy.spatial as sp
from imutils import contours
from imutils import perspective
from scipy.spatial import distance as dist
from final_rtom import *
from badacc import *
from annotated_text import annotated_text
st.write('<style>.css-1yjuwjr{font-size:22px;}', unsafe_allow_html=True)
st.write('<style>.st-af{font-size:1.3rem;}', unsafe_allow_html=True)
st.write('<style>.st-cw{height:1.6rem;}', unsafe_allow_html=True)
st.write('<style>.st-d2{width:1.6rem;}', unsafe_allow_html=True)
st.write('<style>.st-d6{height:8px;}', unsafe_allow_html=True)
st.write('<style>.st-d7{width:8px;}', unsafe_allow_html=True)
st.write('<style>code{font-size:1.1em;}', unsafe_allow_html=True)
st.write('<style>p{font-size:1.2rem;}', unsafe_allow_html=True)



st.title("Real Time Object Measurement")
annotated_text(("open","CV","#269e98"),("with","python","#d16c06"),)
st.subheader("This app allows you to measure objects in real time with your webcam!")
st.text("We use OpenCV and Streamlit for this demo")
if st.checkbox("Main Checkbox"):
    st.text("Are you ready?")



st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}', unsafe_allow_html=True)

options = st.sidebar.radio("Choose",('Real','Static'))
if options == 'Real':
    with st.sidebar:
        with st.expander("INSTRUCTIONS TO USE IPWEBCAM"):
            #st.sidebar.title("INSTRUCTIONS TO USE IPWEBCAM")
                st.write("1.Download the IP Webcam App from PlayStore on your Mobile")
                st.write("2.Open the App")
                st.write("3.Scroll down and click on Start Server. Your Mobile's Camera will be turned on")
                st.write("4.Notedown the IP Address displayed")
             
        with st.expander("WHAT IS AN ARUCO MARKER?"):
            st.write("""
                An aruco marker is a fiducial marker that is placed on the object or scene being imaged. 
                It is a binary square with black background and boundaries and a white generated pattern within it that uniquely identifies it.
                The black boundary helps making their detection easier. They can be generated in a variety of sizes.
                The idea is that you print these markers and put them in the real world.
                You can photograph the real world and detect these markers uniquely.
            """)
            st.warning("Real time measurement won't workout without arUco marker")
            st.info('Please do find the instructions and link to download the arUco marker below ')
        
        with st.expander("INSTRUCTIONS TO USE ARUCO"): 
            #st.sidebar.title("INSTRUCTIONS TO USE ARUCO")
            
            st.write("1.Download the aruco marker PDF")
            st.write("2.Print the PDF")
            st.write("3.Place object to be measured beside arUco marker")
            st.write("4.Enter IP address")
            st.write("5.Point webcam such that arUco marker and object are in the same frame")
            st.write("6.Enjoy the real-time accuracy !!")
            
            
            st.sidebar.subheader("Download ArucoMarker")
            with open("ar6.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()

            st.sidebar.download_button(label="Aruco_Marker",
                                data=PDFbyte,
                                file_name="Aruco_marker.pdf",
                                mime='application/octet-stream')
        st.markdown('##')
        
            
        
           
    #st.success("You are measuring in real time")
    try:    
        live()
    except:
        pass
elif options == 'Static':
    try:
        with st.sidebar:
            with st.expander("INSTRUCTIONS TO USE"):
                
                st.info("""While takingapicture make sure to place your reference object on the left most part of your picture.
                        Your reference object can be anything of your choice,provided you know the width of the said object.""")
                st.image("prop.jpeg",caption='Coin in this particular case')
                st.warning('Width of the reference object is in INCHES ')
        static()
    except:
        pass
