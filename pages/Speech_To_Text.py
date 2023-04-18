import streamlit as st
from functions import api_functions as api_f
import pandas as pd
import constants as k

st.set_page_config(page_title="Speech To Text", page_icon="", layout="wide")

st.title("Speech to Text [🔗](https://cloud.ibm.com/apidocs/speech-to-text)")

tab1, tab2 = st.tabs(["Synthesize", "List Voices"])

with tab1:
    print("aaa")

with tab2:
    VOICES = api_f.GET_VOICES()

    ret_fields = st.multiselect('Returned Fields:', ["gender","custom_pronunciation","voice_transformation","name","customizable","description","language","url"],["gender","name","language"])
    df = pd.DataFrame(columns=ret_fields, index=range(len(VOICES['voices'])))
    i = 0
    for lt in VOICES['voices']:
        d = {}
        if 'gender' in ret_fields: d['gender'] = lt['gender']
        if 'custom_pronunciation' in ret_fields: d['custom_pronunciation'] = lt['supported_features']['custom_pronunciation']
        if 'voice_transformation' in ret_fields: d['voice_transformation'] = lt['supported_features']['voice_transformation']
        if 'name' in ret_fields: d['name'] = lt['name']
        if 'customizable' in ret_fields: d['customizable'] = lt['customizable']
        if 'description' in ret_fields: d['description'] = lt['description']
        if 'language' in ret_fields: d['language'] = lt['language']
        if 'url' in ret_fields: d['url'] = lt['url']

        df.loc[i] = pd.Series(d)
        i += 1

    st.dataframe(df, use_container_width=True)
