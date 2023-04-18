
import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['PSG-SIM-3Hd(kQ5d']).generate()
print(hashed_passwords)