# # import streamlit as st
# import requests

# # ✅ Set page config as the first command
# st.set_page_config(page_title="AI Study Assistant", page_icon="🤖", layout="wide")

# def show():
#     st.header("🤖 AI Study Assistant (ChatGPT)")

#     # Try embedding ChatGPT
#     iframe_html = """
#     <iframe src="https://chatgpt.com/" width="100%" height="600" onerror="this.parentElement.innerHTML='<a href=https://chatgpt.com/ target=_blank><button style=background-color:#FF4B4B;color:white;padding:10px;border:none;border-radius:5px;>Open ChatGPT 🔗</button></a>';">
#     </iframe>
#     """
#     st.markdown(iframe_html, unsafe_allow_html=True)

#     # Fallback button if iframe doesn't work
#     st.write("If ChatGPT does not load above, click below to open it in a new tab:")
#     st.markdown(
#         '<a href="https://chatgpt.com/" target="_blank">'
#         '<button style="background-color:#FF4B4B;color:white;padding:10px;border:none;border-radius:5px;">'
#         'Open ChatGPT 🔗'
#         '</button></a>',
#         unsafe_allow_html=True
#     )

# show()
