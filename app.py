import streamlit as st
# from py_wanderer import ALGORITHMS, HEURISTICS
import pandas as pd
import pyodbc
# from io import StringIO
# import numpy as np
# import streamlit_authenticator as stauth
# from streamlit_authenticator import Hasher

# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")

# names = ["4200 NW 19th Street", "44 West Flagler St", "200 SE 1st St"]
# names = ["a", "b", "c"]
# usernames = names

# # passwords = ["password1", "password2", "password3"]
# # Hasher = Hasher()
# # hashed_passwords = Hasher.hash_list(passwords)

# # print(hashed_passwords)

# hashed_passwords = ['$2b$12$dyBhYgyrq71/53K2TE9T5.5mHr.ncDVAnzs567UCp/k8ymHjGWMli', 
#                     '$2b$12$ZFu1ejtksWJFPqHr5LdtFuhHwln3ZcuoRrzpRd.I0mMopviI0pyi6', 
#                     '$2b$12$wjvupXZf7yGc76iEcFZMJuACx3zvyCawEgZzN44NqRemiOfAYvtOK']

# credentials = {"usernames": {}}

# for uname, name, pwd in zip(usernames, names, hashed_passwords):
#     credentials["usernames"][uname] = {
#         "name": name,
#         "password": pwd
#     }



# authenticator = stauth.Authenticate(
#     credentials,
#     cookie_name="client_dashboard_cookie",
#     cookie_key="abcdef",
#     cookie_expiry_days=7
# )

# login_result = authenticator.login(location='main', key='Login')
# st.write(login_result)
# if login_result is not None:
#     name, authentication_status, username = login_result
# else:
#     name = authentication_status = username = None


# if authentication_status is False:
#     st.error("Username or password is incorrect")
# elif authentication_status is None:
#     st.warning("Please enter your username and password")
# elif authentication_status:
#     authenticator.logout("Logout", "sidebar")
#     st.sidebar.write(f"Welcome, {name} 👋")

def get_data():
    # conn = pyodbc.connect(
    #     r"DRIVER={ODBC Driver 17 for SQL Server};"
    #     r"SERVER=localhost\SQLEXPRESS;"
    #     r"DATABASE=OPUS;"
    #     r"Trusted_Connection=yes;"
    #     )
    # df = pd.read_sql("Select submission_date Date, job Job, employee Employee, form_name Form, link PDF from submissions", conn)
    df = pd.read_csv("submissions.csv")
    df = df[df["Job"] == "4200 NW 19th Street"]
    # df = df.drop("Job", axis = 1)
    # df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df["Form"] = [x.replace("_", " ") for x in df["Form"]]
    return df

df = get_data()

if st.button("Refresh Data"):
    df = get_data()

with st.expander("Submissions"):
    
    employees = sorted(df["Employee"].dropna().unique())
    selected_employee = st.multiselect("Filter by employee:", employees)

    forms = sorted(df["Form"].dropna().unique())
    selected_form = st.multiselect("Filter by form:",forms)

    if selected_form and selected_employee:
        filtered_df = df[df["Form"].isin(selected_form)]
        filtered_df = filtered_df[filtered_df["Employee"].isin(selected_employee)]
    elif selected_form:
        filtered_df = df[df["Form"].isin(selected_form)]
    elif selected_employee:
        filtered_df = df[df["Employee"].isin(selected_employee)]
    else:
        filtered_df = df

    table_html = filtered_df.to_html(escape=False, index=False)
    table_html = table_html.replace('style="text-align: right;"', '')  # optional cleanup
    table_html = table_html.replace('border="1" class="dataframe"', 'class="dataframe"')  # cleaner look
    table_html = table_html.replace('style="width: 100%;"', '')  # THIS removes the extra spacing problem


    display_df = filtered_df.copy()
    display_df["PDF"] = display_df["PDF"].apply(lambda x: f'<a href="{x}" target="_blank">PDF</a>')

    st.markdown(
        f"""
        <div style="max-height:500px; overflow-y:auto;">
            {display_df.to_html(escape=False, index=False)}
        </div>
        """,
        unsafe_allow_html=True
    )

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="submissions.csv",
        mime="text/csv"
    )



with st.expander("Form"):
    with st.form("my_form"):
         st.write("Form Title")
         st.text_input("Enter your name")
         st.radio("Choose one:", ["Option 1", "Option 2", "Option 3"])
         st.number_input("Enter a number between 1 and 10", -10, 10)
         st.date_input("Select Date")
         st.time_input("Select Time")
         st.color_picker("Pick a color")
         slider_val = st.slider("Form slider")
         checkbox_val = st.checkbox("Form checkbox")
         st.file_uploader("Upload file")
         st.camera_input("Upload image")
    
    
         submitted = st.form_submit_button("Submit")
         if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)





