import streamlit as st
from functions import api_functions as f
import constants as k
import pandas as pd

st.set_page_config(page_title="IBM API GUI", page_icon="⚡", layout="wide")

st.title("IBM API Configuration [🔗](https://cloud.ibm.com/apidocs)")

k.api_key = st.text_input("API Key", k.api_key)
disable_button = (k.api_key == "")

#if st.button("GET IAM TOKEN", disabled=disable_button):
    #IBM_Cloud_Instance.update_values(api_key)
    #st.write(IBM_Cloud_Instance.get_token())

if st.button("GET RESOURCES", disabled=disable_button):
    #st.write(IBM_Cloud_Instance.get_resource_instances())
    list_resources = f.get_resource_instances()

    for r in list_resources:
        with st.expander(f"{r} Services ({len(list_resources[r])})"):
            #for r_instance in list_resources[r]:
                #st.write(r_instance['name'])
            cols = ['name', 'guid', 'region_id']
            df = pd.DataFrame(columns=cols, index=range(len(list_resources[r])))
            i = 0
            for lr in list_resources[r]:
                d = {'name': lr['name'],
                     'guid': lr['guid'],
                     'region_id': lr['region_id']}

                df.loc[i] = pd.Series(d)
                i += 1

            st.dataframe(df, use_container_width=True)

#if st.button("GET RESOURCE", disabled=disable_button):
    #st.write(IBM_Cloud_Instance.get_resource_instance(guid="90e3b10f-803e-4b5d-9d86-abca677865be"))

#if st.button("GET KEY", disabled=disable_button):
    #IBM_Cloud_Instance.update_values(api_key)
    #st.write(IBM_Cloud_Instance.get_resource_key())
