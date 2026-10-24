import requests
import streamlit as st

# Page Configuration (Gemini jaisa look)
st.set_page_config(
    page_title="Siya AI", page_icon="🤖", layout="centered"
)

st.title("🤖 Siya AI Assistant")
st.write("Aapka apna AI Assistant - Powered by Llama 3")

# Sidebar - Ngrok URL
st.sidebar.header("⚙️ Server Settings")
ngrok_url = st.sidebar.text_input(
    "Enter your Ngrok URL:", placeholder="https://xxxx.ngrok-free.app"
)

# Initialize Chat History
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Siya se kuch bhi puchen..."):
  if not ngrok_url:
    st.error("Kripya pehle sidebar me apna Ngrok URL dalein!")
  else:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # Clean URL format
    url = ngrok_url.strip().rstrip("/") + "/api/generate"

    # Send request to your local Llama 3
    try:
      payload = {
          "model": "llama3",
          "prompt": prompt,
          "stream": False,
      }
      with st.spinner("Siya soch rahi hai..."):
        response = requests.post(url, json=payload, timeout=60)

      if response.status_code == 200:
        reply = response.json().get("response", "Koi javab nahi mila.")
        with st.chat_message("assistant"):
          st.markdown(reply)
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
      else:
        st.error(f"Server Error: {response.status_code}")
    except Exception as e:
      st.error(f"Connect nahi ho pa raha hai. Error: {e}")