
from hashlib import new
import logging

import streamlit as st

from src.services.nethound import get_networks
from src.logic.timeseries import get_timeseries
from src.logic.graph import new_timeseries_plot

LOGGER = logging.getLogger(__name__)

# wrap network retrieval function in cache
# decorator
get_networks = st.cache(get_networks)

# get all networks from API
networks = get_networks()
if networks is None:
    raise

st.write('Select a network on the left to view timeseries data for a given network. Use the slider to adjust the timeframe over which the data is being viewed.')
st.write("-" * 34)
# add select box to allow users to select network
selected_network = st.sidebar.selectbox('Select a network', [n.network_name for n in networks])

# add slider to configure time range
timerange_hours = st.slider('Historical data range (hours)', value=3, min_value=1, max_value=12)

ts = get_timeseries(networks, selected_network, timerange_hours)

with st.container():
    # write message to frontend if no
    # data is found. else generate plot
    if ts.shape[0] == 0:
        st.write('No data to display!')
    else:
        plot = new_timeseries_plot(ts)
        st.altair_chart(plot, use_container_width=True)



