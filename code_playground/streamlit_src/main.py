import streamlit as st

import webpage

import app_home
import cheat_sheet


PAGES = {
    "Home": app_home,
    "Quick Commands": cheat_sheet,
}


def main():
    """Main function of the App"""
    webpage.page_layout("wide")

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    st.sidebar.title("Contribute")
    st.sidebar.info(
        "You are very welcome to **contribute** your awesome "
        "comments, questions, and resources as "
        "[issues](https://forms.clickup.com/f/1zqf-13937/0V03FDIN7FXSL0R6XV) or "
        "[pull requests](https://github.com/gadventures/bookkeeper/blob/master/bookkeeper/pulls) "
        "to the [source code](https://github.com/gadventures/bookkeeper/blob/master/bookkeeper). "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        "This app is maintained in order to provide easy recall. "
        "Inspired by Awesome Streamlit [source code](https://github.com/MarcSkovMadsen/awesome-streamlit) "
    )

    page = PAGES[selection]
    with st.spinner(f"Loading {selection} ..."):
        webpage.write_page(page)


if __name__ == "__main__":
    main()
