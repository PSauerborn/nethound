import logging

import altair as alt
import pandas as pd


LOGGER = logging.getLogger(__name__)


def new_timeseries_plot(data: pd.DataFrame) -> alt.Chart:
    """Function used to generate new chart

    Returns:
        alt.Chart: [description]
    """

    x_axis = alt.Axis(
        tickCount=5,
        title='Event Timestamp',
        labelPadding=10,
        titlePadding=10)

    y_axis = alt.Axis(
        title='Download Speed (MB)',
        labelPadding=10,
        titlePadding=10)
    # generate x element with custom axis
    x = alt.X('event_timestamp:T', axis=x_axis)
    y = alt.Y('download_speed:Q', axis=y_axis)
    chart = alt.Chart(data).mark_line().encode(
        x=x,
        y=y
    )
    return chart