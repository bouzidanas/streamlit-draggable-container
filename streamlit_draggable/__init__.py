import os
import streamlit.components.v1 as components
import streamlit as st

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Get javascript code from file
with open("streamlit_drag_and_drop.js", "r") as file:
    js_code = file.read()

html = """
<script>""" + js_code + """    
</script>
<div class='elim'></div>
"""

def init():
    components.html(html)

def draggable_container(*args, handle=False, destination=False, **kwargs):
    container = st.container(*args, **kwargs)
    with container:
        classes = []
        if not handle:
            classes.append('no-drag-handle')
        if not destination:
            classes.append('no-destination')
        elif type(destination) == str:
            classes.append("dest-" + destination)
        elif type(destination) == list:
            # for each element in the list, prepend "dest-" to each element and add them to the classes list
            classes += ["dest-" + dest for dest in destination]

        st.markdown("<div class='draggable-parent elim " + " ".join(classes) + "'></div>", unsafe_allow_html=True)

    return container

def destination_container(name, *args, **kwargs):
    container = st.container(*args, **kwargs)
    with container:
        st.markdown("<div class='destination-parent elim dz-" + name + "'></div>", unsafe_allow_html=True)

    return container

if not _RELEASE:
    _component_func_init = components.declare_component(
        # We give the component a simple, descriptive name ("streamlit_execute"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_execute_init",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:5173",
    )
    _component_func_run = components.declare_component("streamlit_execute_run", url="http://localhost:5174")
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component("streamlit_draggable", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def dnd_observer(key=""):
    """Create a new instance of "dnd_observer".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(key=key, default={"id": "", "code":"", "status":"", "value":"", "stdout":""})

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value

if not _RELEASE:
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

    container3 = draggable_container(border=True)

    with container3:
        st.write("This is the second draggable container")
        st.info("This one has no drag handle. Grab it from anywhere inside the container.")
        st.warning("Now that every mouse click and drag is treated as an attempt to move this container, you can no longer select text inside the container.")
