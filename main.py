from types import NoneType
from cem import sea
import streamlit as st
import pandas as pd
import numpy as np
from itertools import product
from PIL import Image

st.write("# Wave calculations")
image = Image.open('./c_t.png')

st.info("Report a bug ? pacourbet@cieletterre.net")
col1, col2, col3 = st.columns(3)
with col2:
    st.image(image)

mode = st.radio("Select mode", ["batch", "single"])

if mode == "single":
    col1, col2, col3 = st.columns(3)
    with col2:
        depth = st.number_input('Water depth [m]', 20.0)
    col1, col2 = st.columns(2)
    with col1:
        windSpeed = st.number_input('Wind speed (3s) at 10 m [m/s]', 30.0)
    with col2:
        fetch = st.number_input('Fetch [m]', 100.0)

    u_tmin, tmin, hs, tp, lp = sea(windSpeed, fetch, depth)

    if st.button("Run"):
        col1, col2= st.columns(2)
        with col1:
            st.write(f"Hs [m] = {round(hs, 2)}")
        with col2:
            st.write(f"Tp [s] = {round(tp, 2)}")

elif mode == "batch":
    col1, col2, col3 = st.columns(3)
    with col2:
        depth = st.number_input('Water depth [m]', 20)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Wind speed (3s) at 10 m [m/s]")
        windSpeed_start = st.number_input('start range', 0)
        windSpeed_end = st.number_input('end range', 70)
        wind_step = st.number_input('step', 5)
    with col2:
        st.markdown("##### Fetch [m]")
        fetch_start = st.number_input('start range', 5)
        fetch_end = st.number_input('end range', 100)
        fetch_step = st.number_input('step', 10)

    speeds = np.arange(windSpeed_start, windSpeed_end, wind_step)
    fetchs = np.arange(fetch_start, fetch_end, fetch_step)
    hss = np.zeros((len(speeds), len(fetchs)))
    tps = np.zeros((len(speeds), len(fetchs)))

    if st.button("Run"):

        for i, j in product(range(len(speeds)), range(len(fetchs))):
            try:
                u_tmin, tmin, hs, tp, lp = sea(speeds[i], fetchs[j], depth)
            except AttributeError:
                hs, tp = 0, 0
            hss[i, j] = hs
            tps[i, j] = tp

        df_hs = pd.DataFrame(columns=fetchs, index=speeds, data=hss)
        df_tp = pd.DataFrame(columns=fetchs, index=speeds, data=tps)

        st.success("Matrices generated")
        st.balloons()

        st.download_button("Download hs matrix as csv",
        data=df_hs.to_csv(),
        file_name="hs.csv",
        mime='text/csv')

        st.download_button("Download tp matrix as csv",
        data=df_tp.to_csv(),
        file_name="tp.csv",
        mime='text/csv')
        

        