import streamlit as st
from functions import api_functions as f
import constants as k
from classes import WLT
import pandas as pd

service_name = "Language Translator"
service_webpage = "https://cloud.ibm.com/apidocs/language-translator"

st.set_page_config(page_title=service_name, page_icon="", layout="wide")

st.title(service_name + " [🔗](" + service_webpage + ")")

# if no api_key is shown
if k.api_key == "":
    st.markdown(f'<p style="color:#ff0000;">️⚠️  No API Key. Insert one in the Main page️ ⚠️</p>', unsafe_allow_html=True)
else:
    # if api_key is inserted find all instances from ibm cloud
    wlt_instances = f.get_resource_instances_by_type("language-translator")

    if len(wlt_instances) == 0:
        st.write("No instances of '" + service_name + "'. Create one at [🔗](" + service_webpage + ")")
    else:
        col_text, col_instance = st.columns(2)
        with col_text:
            st.subheader('Select Instance:')
        with col_instance:
            current_instance = st.selectbox('', tuple(wlt_instances.keys()), label_visibility='collapsed')
        
        # create instance of class WLT
        WLT_Instance = WLT.WLT(wlt_instances[current_instance]['name'],
                       wlt_instances[current_instance]['guid'],
                       wlt_instances[current_instance]['region_id'])

        tab1, tab2, tab3 = st.tabs(["Translate", "List Supported Languages", "List Models"])

        with tab1:
            col_input, col_params = st.columns(2)

            # INPUT
            with col_input:
                st.subheader('Input:')
                input_translation = st.text_area("", "What's your name?", label_visibility='collapsed')

            # PARAMS
            with col_params:
                st.subheader('Parameters:')
                lang_model = st.selectbox('', ("en-it", "it-en", "en-es"), label_visibility='collapsed')

            # BUTTON
            disable_button = (WLT_Instance.api_key == "") | (WLT_Instance.url == "")
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
                translate_button = st.empty
                translate_button = st.button(":blue[Translate]", disabled=disable_button)

            # OUTPUT
            st.subheader('Output:')
            output_translation = st.empty()
            output_translation.text_area("", "", label_visibility='collapsed')
            
            if translate_button:
                output_translation.text_area("", WLT_Instance.translate(input_translation, lang_model))

        with tab2:
            if st.button("Get Languages", disabled=disable_button):
                list_languages = WLT_Instance.get_languages()

                ret_fields = st.multiselect('Returned Fields:', ["language","language_name","native_language_name","country_code","words_separated","direction","supported_as_source","supported_as_target","identifiable"],["language","language_name"])
                df = pd.DataFrame(columns=ret_fields, index=range(len(list_languages['languages'])))
                i = 0
                for lt in list_languages['languages']:
                    d = {}
                    if 'language' in ret_fields: d['language'] = lt['language']
                    if 'language_name' in ret_fields: d['language_name'] = lt['language_name']
                    if 'native_language_name' in ret_fields: d['native_language_name'] = lt['native_language_name']
                    if 'country_code' in ret_fields: d['country_code'] = lt['country_code']
                    if 'words_separated' in ret_fields: d['words_separated'] = lt['words_separated']
                    if 'direction' in ret_fields: d['direction'] = lt['direction']
                    if 'supported_as_source' in ret_fields: d['supported_as_source'] = lt['supported_as_source']
                    if 'supported_as_target' in ret_fields: d['supported_as_target'] = lt['supported_as_target']
                    if 'identifiable' in ret_fields: d['identifiable'] = lt['identifiable']

                    df.loc[i] = pd.Series(d)
                    i += 1

                st.dataframe(df, use_container_width=True)

        with tab3:
            if st.button("Get Models", disabled=disable_button):
                list_models = WLT_Instance.get_models()

                ret_fields = st.multiselect('Returned Fields:',
                                            ["model_id","source","target","base_model_id","domain","customizable","default_model","owner","status","name","training_log"],
                                            ["model_id", "source", "target"])
                df = pd.DataFrame(columns=ret_fields, index=range(len(list_models['models'])))
                i = 0
                for lt in list_models['models']:
                    d = {}
                    if 'model_id' in ret_fields: d['model_id'] = lt['model_id']
                    if 'source' in ret_fields: d['source'] = lt['source']
                    if 'target' in ret_fields: d['target'] = lt['target']
                    if 'base_model_id' in ret_fields: d['base_model_id'] = lt['base_model_id']
                    if 'domain' in ret_fields: d['domain'] = lt['domain']
                    if 'customizable' in ret_fields: d['customizable'] = lt['customizable']
                    if 'default_model' in ret_fields: d['default_model'] = lt['default_model']
                    if 'owner' in ret_fields: d['owner'] = lt['owner']
                    if 'status' in ret_fields: d['status'] = lt['status']
                    if 'name' in ret_fields: d['name'] = lt['name']
                    if 'training_log' in ret_fields: d['training_log'] = lt['training_log']

                    df.loc[i] = pd.Series(d)
                    i += 1

                # st.table(df)
                st.dataframe(df, use_container_width=True)

