from typing import Literal

import streamlit as st


def get_user_name() -> Literal["John"]:
    return "John"


with st.echo():
    # Everything inside this block will be both printed to the screen
    # and executed.

    def get_punctuation() -> Literal["!!!"]:
        return "!!!"

    greeting = "Hi there, "
    value: Literal["John"] = get_user_name()
    punctuation: Literal["!!!"] = get_punctuation()

    st.write(greeting, value, punctuation)

# And now we're back to _not_ printing to the screen
foo = "bar"
st.write("Done!")
