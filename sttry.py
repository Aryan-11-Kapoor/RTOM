import streamlit as st

st.title("Real Time Object Measurement")
st.subheader("This app allows you to measure objects in real time with your webcam!")
st.text("We use OpenCV and Streamlit for this demo")
if st.checkbox("Main Checkbox"):
    st.text("Are you ready?")



with st.sidebar:
   with st.expander("What is an aruco marker?"):
     st.write("""
        An aruco marker is a fiducial marker that is placed on the object or scene being imaged. 
        It is a binary square with black background and boundaries and a white generated pattern within it that uniquely identifies it.
        The black boundary helps making their detection easier. They can be generated in a variety of sizes.

        The idea is that you print these markers and put them in the real world.
         You can photograph the real world and detect these markers uniquely.
     """)
   
     st.sidebar.text("Download ArucoMarker")
     st.sidebar.title("INSTRUCTIONS TO USE ARUCO")
      
     st.sidebar.text("1.Download the aruco marker PDF")
     st.sidebar.text("2.Print the PDF")
     st.sidebar.text("3.Place object to be measured beside arUco marker")
     st.sidebar.text("4.Enter IP address")
     st.sidebar.text("5.Point webcam such that arUco marker and object are in the same frame")
     st.sidebar.text("6.Enjoy the real-time accuracy !!")
    
     st.warning("Real time measurement won't workout without arUco marker")
     st.info('Please do find the instructions and link to download the arUco marker below ')
     
    


