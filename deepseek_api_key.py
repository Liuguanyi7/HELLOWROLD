import streamlit as st
import os 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv

DEEPSEEK_KEY=os.getenv("DEEPSEEK_KEY")
DEEPSEEK_URL=os.getenv("DEEPSEEK_URL")

client = OpenAI(api_key=DEEPSEEK_KEY,base_url=DEEPSEEK_URL)

def initialize_app():
  st.set_page_config(page_title="DeepSeek AI Chat",layout="wide",initial_sidebar_state="expanded")
  if "messages" not in st.session_state:
    st.session_state.messages=[]
    st.session_state.messages.append({"role":"system","content":"content"})

def clear_history_chat():
  system_messages=None
  if st.session_state.messages and st.session_state.messages[0]["role"]=="system":
    system_messages=st.session_state.messages[0]
    st.session_state.messages=[]
  if system_messages:
    st.session_state.messages.append(system_messages)
  st.success("clear up")

def handle_dialogue(user_input):
  if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
  try:
    with st.spinner("AI thinking..."):
      api_messages=[]
        for msg in st.session_state.messages:
          api_messages.append({"role":msg["role"],"content":msg["content"]})
    response=client.chat.completions.create(model="deepseek-chat",messages=api_messages,max_tokens=1000,temperature=0.7)
    ai_messages=response.choices[0].message.content
    st.session_state.messages.append({"role":"assistant","content":ai_messages})
  except Exception as e:
    st.error(f"Error:{e}")
    st.session_state.messages.append({"role":"assistant","content":f"somthing was wrong:{str(e)}"})

def setup_ui():
  st.title("deepseek ai chat")
  st.caption("powered by deepseek")

  if st.sidebar.button("clear history chat"):
    clear_history_chat()
    st.rerun()

  for message in st.session_state.messages:
    if message["role"]!="system":
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

  return st.chat_input("please input your question...")

if __name__=="__main__":
  initialize_app()
  user_query=setup_ui()
    if user_query:
      handle_dialogue(user_query)
      st.rerun()

  
