import streamlit as st
import random
import time
import pandas as pd
import os

# 1. Page Config & Setup
st.set_page_config(page_title="Agra Smart Pass", page_icon="🕌")

# Data File Setup
filename = "guest_data.csv"
if not os.path.isfile(filename):
    pd.DataFrame(columns=["Date", "Name", "Phone", "Verified"]).to_csv(filename, index=False)

# 2. Session State Management (Data yaad rakhne ke liye)
if 'step' not in st.session_state:
    st.session_state.step = "register" # Steps: register -> verify -> success
if 'otp' not in st.session_state:
    st.session_state.otp = None
if 'user_details' not in st.session_state:
    st.session_state.user_details = {}

# 3. UI Design
st.title("🕌 Agra Heritage Smart Pass")
st.markdown("---")

# STEP 1: Registration Form
if st.session_state.step == "register":
    st.subheader("📝 Welcome! Please Register")
    name = st.text_input("Aapka Naam")
    phone = st.text_input("Mobile Number (10 Digits)")
    
    if st.button("Get OTP"):
        if len(phone) == 10 and name:
            # Fake OTP Generate karna
            otp = random.randint(1000, 9999)
            st.session_state.otp = otp
            st.session_state.user_details = {"name": name, "phone": phone}
            
            # Screen par OTP dikhana (Asli SMS ki jagah)
            st.warning(f"DEBUG MODE: Aapka OTP hai: {otp} (Asli app mein ye SMS jayega)")
            
            with st.spinner('OTP bheja ja raha hai...'):
                time.sleep(1.5) # Real feel dene ke liye delay
            
            st.session_state.step = "verify"
            st.rerun()
        else:
            st.error("Kripya sahi Naam aur 10-digit Number bharein.")

# STEP 2: OTP Verification
elif st.session_state.step == "verify":
    st.subheader("🔐 Mobile Verification")
    st.info(f"OTP aapke number {st.session_state.user_details['phone']} par bheja gaya hai.")
    
    entered_otp = st.text_input("4-Digit OTP Enter Karein", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verify & Confirm"):
            if str(entered_otp) == str(st.session_state.otp):
                # Data Excel mein save karna
                now = time.strftime("%Y-%m-%d %H:%M")
                new_row = pd.DataFrame([[now, st.session_state.user_details['name'], st.session_state.user_details['phone'], "YES"]], 
                                      columns=["Date", "Name", "Phone", "Verified"])
                new_row.to_csv(filename, mode='a', header=False, index=False)
                
                st.session_state.step = "success"
                st.rerun()
            else:
                st.error("Galat OTP! Dubara koshish karein.")
    with col2:
        if st.button("Back"):
            st.session_state.step = "register"
            st.rerun()

# STEP 3: Success & Digital Pass
elif st.session_state.step == "success":
    st.balloons()
    st.success(f"Adaab {st.session_state.user_details['name']}! Aapka Verified Pass Taiyaar hai.")
    
    # Digital Pass Card
    st.markdown(f"""
    <div style="border: 2px solid #8b0000; padding: 20px; border-radius: 15px; background-color: #fff9f0; text-align: center;">
        <h2 style="color: #8b0000;">AGRA HERITAGE PASS</h2>
        <p><b>Guest:</b> {st.session_state.user_details['name']}</p>
        <p><b>Phone:</b> {st.session_state.user_details['phone']}</p>
        <p style="color: green;"><b>Status: VERIFIED ✓</b></p>
        <hr>
        <p>Present this at <b>Panchhi Petha</b> for 10% Discount!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("New Registration"):
        st.session_state.step = "register"
        st.rerun()
