from functions import api_functions as f

# elif "Cloud Pak for Data":
#     k.CP4D_URL = st.text_input("URL:", "https://cpd-osdu.apps.st-osdu.eni.com")
#     k.CP4D_USERNAME = st.text_input("Username:", "admin")
#     k.CP4D_PASSWORD = st.text_input("Password:", "iHXPmNR59yY0")
#     if st.button("GET CP4D TOKEN"):
#         st.write(api_functions.GET_CP4D_TOKEN(return_json=True))

def GET_CP4D_TOKEN(return_json=False):
    r_cpd_token = f.API_CALL(
        method="POST",
        url=k.CP4D_URL + "/icp4d-api/v1/authorize",
        headers={
            "cache-control": "no-cache",
            "Content-type": "application/json",
        },
        req_data={"username": k.CP4D_USERNAME, "password": k.CP4D_PASSWORD}
    )

    if return_json:
        return r_cpd_token[0]
    else:
        return r_cpd_token[0]['token']