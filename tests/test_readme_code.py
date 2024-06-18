import streamlit as st
import streamlit_draggable as ste

test_code = """
a=1+1
a
"""

st.subheader("Component Test")
response = ste.init(test_code)
st.write(response)

ste.connect()

run_response = ste.run("print(a)")
st.write(run_response)


new_response = ste.run("b=a*3\nb")
st.write(new_response)

third_response = ste.run("b*b + 4")
st.write(third_response)
