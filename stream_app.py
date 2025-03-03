import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title = "Monitoring Report")

# Title
st.title("Monitoring mail data report")

st.subheader("Select the email domain")
domain = st.selectbox("Domain",["Monitoring","Systems","Database","Network"])

if domain=="Monitoring":
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRSt_5jILbpRc74IA2mMT3Fez05g-dFMON6v9xpNGgRFaGUNJeR02Z3gHhcpUE-7WBiG1Xkx2fdCJ0q/pub?output=csv")
    df["Date"] = pd.to_datetime(df["Date"])
elif domain=="Systems":
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTOobaI9oLZ6hQTHWkmyNByYPfGKgZkGvvdD4le5MXxQY0qIkDHfyPFTOYOOh3DRVmf9fhwjNnOzLJX/pub?output=csv")
    df["Date"] = pd.to_datetime(df["Date"])
elif domain=="Database":
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSHQbCsCXt03mS7vKN3rBRcSun17bBQtylXFR7Vmjq5yZ-gWLM0fIEGpkTdWpdTILmAGXSnDT57ska2/pub?output=csv")
    df["Date"] = pd.to_datetime(df["Date"])
elif domain=="Network":
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRomKijOI2uwb3wk1yt1OJn5kFJPbg4ZGjShtVzLUMoliyV0cWqN1R84Og6lmeLKUWwB0anxswIQ-jA/pub?output=csv")
    df["Date"] = pd.to_datetime(df["Date"])

min_date = min(df["Date"].dt.date)
max_date = max(df["Date"].dt.date)

st.text(f"Select the date between {min_date} and {max_date}")
st.subheader("Enter the start and end date to get data")
start_date = st.date_input("Enter the start date in YYYY/MM/DD format")
end_date = st.date_input("Enter the end date in YYYY/MM/DD format")


start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)

column = st.selectbox("Select the data to be displayed", ["Email Count",
                                                          "Day Wise Email Count",
                                                          "Server Wise Count",
                                                          "Service Down Count",
                                                          "Remote Monitoring Emails Count"])


if(st.button('Submit')):
    if column == "Email Count":
        res_df = df.loc[(df["Date"] >= start) & (df["Date"] <= end)]
        st.subheader("Email Count")
        result = res_df.Subject_Heading.value_counts().to_frame().reset_index()
        result = result.rename(columns={"Subject_Heading":"Subject"})
        fig = px.bar(result,x="Subject",y="count",title="Email Count")
        fig.update_layout(title={'text': "Email Count",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
        st.dataframe(result)

    elif column == "Day Wise Email Count":
        res_df = df.loc[(df["Date"] >= start) & (df["Date"] <= end)]
        st.subheader("Day wise email count")
        result = res_df.Date.value_counts().to_frame().sort_values(by="Date").reset_index()
        fig = px.bar(result,x="Date",y="count",title="Day Wise Email Count")
        fig.update_layout(title={'text': "Day Wise Email Count",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
        st.dataframe(result)
        st.text(f"The average email count per day is : {round(res_df['Date'].value_counts().mean())}")

    elif column == "Server Wise Count":
        res_df = df.loc[(df["Date"] >= start) & (df["Date"]<=end)]
        st.subheader("Server wise count")
        result = res_df.Subject_Details.value_counts().to_frame().reset_index()
        fig = px.bar(result,x="Subject_Details",y="count",title="Server wise count")
        fig.update_layout(title={'text': "Server Wise Count",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
        st.dataframe(result)

    elif column == "Service Down Count":
        res_df = df.loc[(df["Date"] >= start) & (df["Date"]<=end)]
        st.subheader("Service Down Count")
        result = res_df.loc[(res_df["Subject_Heading"]=="Service Down")]["Subject_Details"].value_counts().to_frame().reset_index()
        fig = px.bar(result,x="Subject_Details",y="count",title="Service Down Count")
        fig.update_layout(title={'text': "Service Down Count",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
        st.dataframe(result)
    
    elif column == "Remote Monitoring Emails Count":
        res_df = df.loc[(df["Date"] >= start) & (df["Date"]<=end)]
        res_df = res_df.fillna("Remote").reset_index(drop=True)
        st.subheader("Remote Monitoring Emails Count")
        df_result = res_df.loc[res_df["Subject_Heading"].str.contains("Remote", na=False, case=False)].value_counts().to_frame().reset_index()
        result = df_result['Date'].value_counts().to_frame().sort_values(by="Date").reset_index()
        fig = px.bar(result,x="Date",y="count")
        st.dataframe(df_result)
        st.dataframe(result)

    
    st.plotly_chart(fig, use_container_width=False,
                    theme="streamlit", 
                    key=None, 
                    on_select="ignore", 
                    selection_mode=('points', 'box', 'lasso'))






