import streamlit as st
from functions import api_functions as f
import constants as k
from classes import NLU
import pandas as pd

service_name = "Natural Language Understanding"
service_webpage = "https://cloud.ibm.com/apidocs/natural-language-understanding"

st.set_page_config(page_title=service_name, page_icon="", layout="wide")

st.title(service_name + " [🔗](" + service_webpage + ")")

# if no api_key is shown
if k.api_key == "":
    st.markdown(f'<p style="color:#ff0000;">️⚠️  No API Key. Insert one in the Main page️ ⚠️</p>', unsafe_allow_html=True)
else:
    # if api_key is inserted find all instances from ibm cloud
    nlu_instances = f.get_resource_instances_by_type("natural-language-understanding")

    if len(nlu_instances) == 0:
        st.write("No instances of '" + service_name + "'. Create one at [🔗](" + service_webpage + ")")
    else:
        col_text, col_instance = st.columns(2)
        with col_text:
            st.subheader('Select Instance:')
        with col_instance:
            current_instance = st.selectbox('', tuple(nlu_instances.keys()), label_visibility='collapsed')

        # create instance of class WLT
        NLU_Instance = NLU.NLU(nlu_instances[current_instance]['name'],
                       nlu_instances[current_instance]['guid'],
                       nlu_instances[current_instance]['region_id'])

        tab1, tab2 = st.tabs(["Analyze", "List Custom Models"])

        with tab1:
            col_input, col_params = st.columns(2)

            # INPUT
            with col_input:
                st.subheader('Input:')
                input_type = st.radio("",["text", "url", "html"],index=0, horizontal=True, label_visibility='collapsed')
                if input_type == "text":
                    input_analyze = st.text_area("", "Leonardo DiCaprio won Best Actor in a Leading Role for his performance.", label_visibility='collapsed')
                elif input_type == "url":
                    input_analyze = st.text_area("", "www.ibm.com", label_visibility='collapsed')
                elif input_type == 'html':
                    input_analyze = st.text_area("", "<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I love apples! I don't like oranges.</p></body></html>", label_visibility='collapsed')
                
            # PARAMS
            with col_params:
                st.subheader('Parameters:')
                num_categories = st.number_input("n° of categories", step=1, min_value=1, max_value=5)

            # BUTTON
            disable_button = (NLU_Instance.api_key == "") | (NLU_Instance.url == "")
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
                analyze_button = st.empty
                analyze_button = st.button(":blue[Analyze]", disabled=disable_button)

            # OUTPUT
            st.subheader('Output:')
            col_cat, col_class = st.columns(2)

            with col_cat:
                output_cat = st.empty()
                output_cat.text_area("Categories:", "", label_visibility='collapsed')

            with col_class:
                output_class = st.empty()
                output_class.text_area("Classifications:", "", label_visibility='collapsed')

            if analyze_button:
                output_cat.text_area("Categories:", NLU_Instance.categories(input_analyze, input_type, num_categories), label_visibility='collapsed')
                output_class.text_area("Classifications", NLU_Instance.classifications(input_analyze, input_type), label_visibility='collapsed')

        with tab2:
            if st.button("Get Models", disabled=disable_button):
                list_models = NLU_Instance.get_models()

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

