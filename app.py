import streamlit as st
import markdown
import pandas as pd
import streamlit as st
from plotly import express as px
from typing import List, Optional

st.set_page_config(layout="wide")

"""
# VISUALIZO
"""


def main():
    """Main function. Run this to run the app"""

    st.sidebar.title("Model Parameters")
    st.markdown(f'''
        <style>
        section[data-testid="stSidebar"] .css-1oe6wy4 {{width: 25rem; padding: 2rem;}}
        </style>
    ''',unsafe_allow_html=True)
    model = st.sidebar.selectbox(
        'Select Model:',
        (
         'Support Vector Machine',
         'Logistic Regression',
         'Linear Discriminant Analysis',
         'Quadratic Discriminant Analysis',
         'Multilayer Perceptron',
         'Decision Tree',
         'Random Forest',
         'Ada Boost',
         'XG Boost',
         'K Nearest Neigbours'
        )
    )

    dataset = st.sidebar.selectbox(
        'Select Dataset:',
        (
         'Moons',
         'Linearly Separable',
         'Circle',
         'Two Gaussians'
        )
    )

    sample_size = st.sidebar.slider("Sample Size: ", 100, 500, 100, 100)
    noise_level = st.sidebar.slider("Noise Level: ", 0.0, 1.0, 0.0, 0.1)
    st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    threshold = st.sidebar.slider("Threshold: ", 0.0, 1.0, 0.0, 0.1)
    st.sidebar.button("RESET THRESHOLD")

    kernel = st.sidebar.selectbox(
        'Kernel:',
        (
         'Radial Basis Function(RBF)',
         'Linear',
         'Polynomial',
         'Sigmoid'
        )
    )


    cost = st.sidebar.slider("Cost (C) for Stack: ", 100, 500, 100, 100)
    st.sidebar.slider("", 100, 500, 100, 100)

    degree = st.sidebar.slider("Degree:", 100, 500, 100, 100)

    zero_order = st.sidebar.slider("Zero-order Kernel Term:", 100, 500, 100, 100)

    gamma = st.sidebar.slider("Gamma:", 100, 500, 100, 100)
    st.sidebar.slider("*", 100, 500, 100, 100)                                                                           

    shrinking = st.sidebar.radio(
     "Shrinking:",
     ('Enabled', 'Disabled'))

    # My preliminary idea of an API for generating a grid
    with Grid("1 1 1") as grid:
        grid.cell(
            class_="a",
            grid_column_start=2,
            grid_column_end=3,
            grid_row_start=1,
            grid_row_end=2,
        ).markdown("# This is A Markdown Cell")
        grid.cell("b", 2, 3, 2, 3).text("The cell to the left is a dataframe")
        grid.cell("c", 3, 4, 2, 3).plotly_chart(get_plotly_fig())
        grid.cell("d", 1, 2, 1, 3).dataframe(get_dataframe())
        grid.cell("e", 3, 4, 1, 2).markdown("Try changing the **block container style** in the sidebar!")



class Cell:
    """A Cell can hold text, markdown, plots etc."""
    def __init__(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        self.class_ = class_
        self.grid_column_start = grid_column_start
        self.grid_column_end = grid_column_end
        self.grid_row_start = grid_row_start
        self.grid_row_end = grid_row_end
        self.inner_html = ""

    def _to_style(self) -> str:
        return f"""
.{self.class_} {{
    grid-column-start: {self.grid_column_start};
    grid-column-end: {self.grid_column_end};
    grid-row-start: {self.grid_row_start};
    grid-row-end: {self.grid_row_end};
}}
"""

    def text(self, text: str = ""):
        self.inner_html = text

    def markdown(self, text):
        self.inner_html = markdown.markdown(text)

    def dataframe(self, dataframe: pd.DataFrame):
        self.inner_html = dataframe.to_html()

    def plotly_chart(self, fig):
        self.inner_html = f"""
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<body>
    <p>This should have been a plotly plot.
    But since *script* tags are removed when inserting MarkDown/ HTML i cannot get it to work</p>
    <div id='divPlotly'></div>
    <script>
        var plotly_data = {fig.to_json()}
        Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
    </script>
</body>
"""

    def to_html(self):
        return f"""<div class="box {self.class_}">{self.inner_html}</div>"""


class Grid:
    """A (CSS) Grid"""
    def __init__(
        self, template_columns="1 1 1", gap="10px", background_color="#fff", color="#444"
    ):
        self.template_columns = template_columns
        self.gap = gap
        self.background_color = background_color
        self.color = color
        self.cells: List[Cell] = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_html(), unsafe_allow_html=True)

    def _get_grid_style(self):
        return f"""
<style>
    .wrapper {{
    display: grid;
    grid-template-columns: {self.template_columns};
    grid-gap: {self.gap};
    background-color: {self.background_color};
    color: {self.color};
    }}
    .box {{
    background-color: {self.color};
    color: {self.background_color};
    border-radius: 5px;
    padding: 20px;
    font-size: 150%;
    }}
    table {{
        color: {self.color}
    }}
</style>
"""

    def _get_cells_style(self):
        return (
            "<style>" + "\n".join([cell._to_style() for cell in self.cells]) + "</style>"
        )

    def _get_cells_html(self):
        return (
            '<div class="wrapper">'
            + "\n".join([cell.to_html() for cell in self.cells])
            + "</div>"
        )

    def cell(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        cell = Cell(
            class_=class_,
            grid_column_start=grid_column_start,
            grid_column_end=grid_column_end,
            grid_row_start=grid_row_start,
            grid_row_end=grid_row_end,
        )
        self.cells.append(cell)
        return cell






@st.cache
def get_dataframe() -> pd.DataFrame():
    """Dummy DataFrame"""
    data = [
        {"quantity": 1, "price": 2},
        {"quantity": 3, "price": 5},
        {"quantity": 4, "price": 8},
    ]
    return pd.DataFrame(data)

def get_plotly_fig():
    """Dummy Plotly Plot"""
    return px.line(
        data_frame=get_dataframe(),
        x="quantity",
        y="price"
    )

main()