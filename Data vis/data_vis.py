import streamlit as st
import pandas as pd
from datetime import datetime
st.set_page_config(page_title="transactions",page_icon="💰",layout="wide",initial_sidebar_state="expanded")
#must first
st.title("pocket money analyst")
st.markdown("keep track your transactions")
if "transactions" not in st.session_state:
    st.session_state.transactions=[]

with st.sidebar:
    st.header("add a new transactions")
    date=st.date_input("date",datetime.now())
    amount=st.number_input("amount",min_value=0.00,value=10.00,step=0.01)
    category=st.selectbox("category",["snacks","game","toy","other"])
    description=st.text_input("description")
    if st.button("add transaction"):
        if amount > 0:
            new_transaction={
                "date":date,
                "amount":amount,
                "category":category,
                "description":description
            }
            st.session_state.transactions.append(new_transaction)
            st.info("the transaction was record.")
        else:
            st.error("amount must greater than 0.")
            
if st.session_state.transactions:
    df=pd.DataFrame(st.session_state.transactions)
    st.subheader("transactions history")
    st.dataframe(df)
    total_spent=df["amount"].sum()
    st.info(f"total spent :{total_spent:.2f}yuan")
else:
    st.info("you have no transaction.")
st.markdown("---")
st.markdown("### Use tips")
st.markdown("""
1. add of your expenses on the left.
2. check out the chart to see your spending distributed.
""")
