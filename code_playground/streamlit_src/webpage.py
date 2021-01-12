"""Components for the Awesome Streamlit App and other use cases
Hopefully a lot of the components  will be removed again as the streamlit api is extended"""
import base64
import importlib
import logging
import sys
from typing import Any, List

import streamlit as st

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def _reload_module(page):
    """Reloads the specified module/ page
    Arguments:
        page {module} -- A page/ module
    """
    logging.debug(
        """--- Reload of module for live reload to work on deeply imported python modules.
    Cf. https://github.com/streamlit/streamlit/issues/366 ---"""
    )
    logging.debug("2. Module: %s", page)
    logging.debug("3. In sys.modules: %s", page in sys.modules)
    try:
        importlib.import_module(page.__name__)
        importlib.reload(page)
    except ImportError as _:
        logging.debug("4. Writing: %s", page)
        logging.debug("5. In sys.modules: %s", page in sys.modules)


def write_page(page):  # pylint: disable=redefined-outer-name
    """Writes the specified page/module
    Our multipage app is structured into sub-files with a `def write()` function
    Arguments:
        page {module} -- A module with a 'def write():' function
    """
    # _reload_module(page)
    page.write()


def video_youtube(src: str, width="100%", height=315):
    """An extension of the video widget
    Arguments:
        src {str} -- A youtube url like https://www.youtube.com/embed/B2iAodr0fOo
    Keyword Arguments:
        width {str} -- The width of the video (default: {"100%"})
        height {int} -- The height of the video (default: {315})
    """
    st.write(
        f'<iframe width="{width}" height="{height}" src="{src}" frameborder="0" '
        'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" '
        "allowfullscreen></iframe>",
        unsafe_allow_html=True,
    )


def multiselect(
    label: str, options: List[Any], default: List[Any], format_func=str
) -> List[Any]:
    """multiselect extension that enables default to be a subset list of the list of objects
     - not a list of strings.
     Assumes that options have unique format_func representations
     cf. https://github.com/streamlit/streamlit/issues/352
    Arguments:
        label {str} -- A label to display above the multiselect
        options {List[Any]} -- A list of objects
        default {List[Any]} -- A list of objects to be selected by default
    Keyword Arguments:
        format_func {[type]} -- [description] (default: {str})
    Returns:
        [type] -- [description]
    """

    options_ = {format_func(option): option for option in options}
    default_ = [format_func(option) for option in default]
    selections = st.multiselect(
        label, options=list(options_.keys()), default=default_, format_func=format_func
    )
    return [options_[format_func(selection)] for selection in selections]


def webpage_title(body: str):
    """Uses st.write to write the title
    - plus the awesome badge
    - plus a link to the GitHub page
    Arguments:
        body {str} -- [description]
    """

    st.write(
        "## Quick Commands {body}"
        "[:books:]"
        "(https://github.com/lemode/code_playground)".format(body=body)
    )


def page_layout(page_layout):
    st.set_page_config(layout=page_layout)


def write_svg(svg: str):
    """Renders the given svg string.
    Arguments:
        svg {str} -- A string containing svgs
    """
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


def horizontal_ruler(in_sidebar: bool = False):
    """Inserts a horizontal ruler (like <hr> in HTML)
    Keyword Arguments:
        in_sidebar {bool} -- If True the ruler is inserted in the sidebar (default: {False})
    """
    if in_sidebar:
        return st.sidebar.markdown("---")

    return st.markdown("---")


def color(outcome_value):
    if outcome_value == constants.PASS_OUTCOME:
        color = "green"
    elif outcome_value == constants.FAIL_OUTCOME:
        color = "red"
    return "background-color: %s" % color


def generate_final_report(
    df1,
    df1_name=None,
    df2=None,
    df2_name=None,
    df3=None,
    df3_name=None,
    df4=None,
    df4_name=None,
):

    output = io.BytesIO()

    # send data to excel
    writer = pd.ExcelWriter(output, engine="xlsxwriter")

    # pivot summary tab
    if df1:
        df1.to_excel(writer, sheet_name=df1_name, encoding="utf-8", index=False)

    # payables tab
    if df2:
        df2.to_excel(writer, sheet_name=df2_name, encoding="utf-8", index=False)

    # interco tab
    if df3:
        df3.to_excel(writer, sheet_name=df3_name, encoding="utf-8", index=False)

    # exchange rate tab
    if df4:
        df4.to_excel(writer, sheet_name=df4_name, encoding="utf-8", index=False)

    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(byte_value, output_file):
    """
    Generates a link allowing the data in a given panda dataframe to be downloaded

    Arguements
    ---------
        byte_value : convert an .xlsx or any file to bytes encoded
        output_file_name : name of file to be downloaded
    """
    b64 = base64.b64encode(byte_value).decode()  # val looks like b'...'
    return '<a href="data:application/octet-stream;base64,{b64}" download="{output_file}">Download file</a>'.format(
        b64=b64, output_file=output_file
    )  # decode b'abc' => abc
