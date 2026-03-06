import streamlit as st
import random
import requests
import pandas as pd
from datetime import datetime

# --- CONFIG ---
API_KEY = "YOUR_FAST2SMS_API_KEY_HERE" # Apni key yahan dalein

def send_real_otp(phone, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "variables_values": str(otp),
        "route": "otp",
        "numbers": str(phone),
    }
    headers = {"authorization": API_KEY}
    response = requests.get(url, params=payload, headers=headers)
    return response.json()

# --- APP LOGIC ---
st.title("🕌 Agra Heritage Smart Pass")

if 'step' not in st.session_state: st.session_state.step = "register"

if st.session_state.step == "register":
    name = st.text_input("Full Name")
    phone = st.text_input("Mobile Number")
    
    if st.button("Send Real OTP"):
        if len(phone) == 10:
            otp = random.randint(1000, 9999)
            st.session_state.otp = otp
            st.session_state.temp_data = {"name": name, "phone": phone}
            
            # Asli SMS Bhejna
            res = send_real_otp(phone, otp)
            if res.get("return"):
                st.session_state.step = "verify"
                st.success("OTP sent to your phone!")
                st.rerun()
            else:
                st.error("SMS Error! Balance check karein.")

elif st.session_state.step == "verify":
    entered_otp = st.text_input("Enter OTP received on SMS", type="password")
    if st.button("Verify"):
        if str(entered_otp) == str(st.session_state.otp):
            st.session_state.step = "success"
            st.rerun()
        else:
            st.error("Invalid OTP!")

elif st.session_state.step == "success":
    st.balloons()
    st.success(f"Welcome to Agra, {st.session_state.temp_data['name']}!")
    # Yahan aapka Digital Pass Design aayega
