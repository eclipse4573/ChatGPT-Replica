import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import os

# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

#Initializing session state variables.

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): #Initializing the chat message history, "messages" is one of the keys of the session state dictionary.
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

#Initializing ChatOpenAI and ConversationChain.
# llm = ChatOpenAI(model_name="gpt-4o-mini")
# llm = ChatGoogleGenerativeAI(model = "gemini-pro")
llm = ChatOpenAI(model = "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
                      openai_api_key = st.secrets["TOGETHER_API_KEY"],
                      openai_api_base = "https://api.together.xyz/v1"
)

conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

#Creating the user interface.
st.title("Conversational Chatbot")
st.subheader("Simple Chat Interface for LLMs by Tanishka Sehgal")

# prompt = st.chat_input('Ask a question...')
# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})

if prompt := st.chat_input("Ask a question..."): #Prompting for user input and saving to chat history.
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: #Displaying the previous chat messages.
    if message["role"] == "assistant":
        with st.chat_message(message["role"], avatar = "🤖"): #Using streamlit_chat.    
            st.write(message["content"])
    else:
        with st.chat_message(message["role"], avatar = "🏋️‍♀️"): 
            st.write(message["content"])

#If the last message is not from the assistant, generate a new response.
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input = prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) #Adding the response to the message history.
