import streamlit as st
from __init__ import *

init()

st.title("Draggable containers demo")
st.write("This is a demo testing some javascript and css customizations to make Streamlit containers draggable.")

container = draggable_container(handle=True, border=True)

with container:
    st.write("This is a draggable container with a handle. Grab the handle to move it around.")
    title = st.text_input("Movie title", "Life of Brian")
    st.write("The current movie title is", title)
    # add a drag handle with a repeating dot pattern
    st.markdown("<div class='drag-handle' style='height: 15px; width: 100%; display: flex; justify-content: center; align-items: center; border: 1px solid #444444; border-radius: 3px; cursor: pointer;margin-bottom: 0.5rem;margin-top:-0.5rem;'><div style='height: 3px; width: 3px; background-color: #444444; border-radius: 50%; margin: 0 2px;'></div><div style='height: 3px; width: 3px; background-color: #444444; border-radius: 50%; margin: 0 2px;'></div><div style='height: 3px; width: 3px; background-color: #444444; border-radius: 50%; margin: 0 2px;'></div></div>", unsafe_allow_html=True)
st.write("You can customize the drag handle and drop location indicators. Note that these indicators dissapear when the mouse is not over a set drop destination. If no drop destination is designated, the parent container will be automatically set as the drop destination.")

container2 = st.expander("Buttons")
with container2:
    if st.button("Click me"):
        st.write("Button clicked!")

st.code("print('hello')")

container3 = draggable_container(border=True, destination="test1")

with container3:
    st.write("This is the second draggable container")
    st.info("This one has no drag handle. Grab it from anywhere inside the container.")
    st.warning("Now that every mouse click and drag is treated as an attempt to move this container, you can no longer select text inside the container.")

container4 = destination_container("test1", border=True)

with container4:
    st.write("This is destination container")
    st.info("This container requires a name which you will pass to the draggable elements so that they are allowed to be dropped here.")