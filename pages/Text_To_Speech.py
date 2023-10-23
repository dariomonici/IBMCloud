import os

import streamlit as st
from functions import api_functions as f
from classes import TTS
import pandas as pd
import constants as k

service_name = "Text to Speech"
service_webpage = "https://cloud.ibm.com/apidocs/text-to-speech"

st.set_page_config(page_title=service_name, page_icon="", layout="wide")

st.title(service_name + " [🔗](" + service_webpage + ")")

# if no api_key is shown
if k.api_key == "":
    st.markdown(f'<p style="color:#ff0000;">️⚠️  No API Key. Insert one in the Main page️ ⚠️</p>', unsafe_allow_html=True)
else:
    # if api_key is inserted find all instances from ibm cloud
    tts_instances = f.get_resource_instances_by_type("text-to-speech")

    if len(tts_instances) == 0:
        st.write("No instances of '" + service_name + "'. Create one at [🔗](" + service_webpage + ")")
    else:
        col_text, col_instance = st.columns(2)
        with col_text:
            st.subheader('Select Instance:')
        with col_instance:
            current_instance = st.selectbox('', tuple(tts_instances.keys()), label_visibility='collapsed')

        # create instance of class WLT
        TTS_Instance = TTS.TTS(tts_instances[current_instance]['name'],
                               tts_instances[current_instance]['guid'],
                               tts_instances[current_instance]['region_id'])

        tab1, tab2 = st.tabs(["Synthesize", "List Voices"])

        with tab1:
            # INPUT
            st.subheader('Input:')
            text_to_synthesize = st.text_input("", "", label_visibility='collapsed')

            # BUTTON
            disable_button = (TTS_Instance.api_key == "") | (TTS_Instance.url == "") | (text_to_synthesize == "")
            col1, col2, col3 , col4, col5 = st.columns(5)

            with col1:
                pass
            with col2:
                pass
            with col4:
                pass
            with col5:
                pass
            with col3 :
                synth_button = st.empty
                synth_button = st.button(":blue[Synthesize]", disabled=disable_button)

            # OUTPUT
            st.subheader('Output:')
            audio_output = st.empty()

            if synth_button:
                TTS_Instance.synthesize(text_to_synthesize)

                audio_file = open('data/tts/tts_audio.wav', 'rb')
                audio_bytes = audio_file.read()

                audio_output.audio(audio_bytes, format='audio/wav')

        with tab2:
            disable_button = (TTS_Instance.api_key == "") | (TTS_Instance.url == "")
            if st.button("Get Voices", disabled=disable_button):
                list_voices = TTS_Instance.get_voices()

                ret_fields = st.multiselect('Returned Fields:', ["gender", "custom_pronunciation","voice_transformation","name","customizable","description","language","url"],["gender","name","language"])
                df = pd.DataFrame(columns=ret_fields, index=range(len(list_voices['voices'])))
                i = 0
                for lt in list_voices['voices']:
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
