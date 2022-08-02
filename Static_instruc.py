import streamlit as st


with st.sidebar:
    st.title("Static object Measurement !",)
   
    with st.expander("Instructions to use "):
        st.info("""While taking a picture make sure to place your reference object on the left most part of your picture.
                Your reference object can be anything of your choice , provided you know the width of the said object.
        
                """)
        st.image("prop.jpeg",caption='Coin in this particular case')
   
        st.warning("Width of the reference object is in INCHES")
     
    
    
 