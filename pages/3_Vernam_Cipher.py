import random

import streamlit as st

from ciphers import (
    vernam_encrypt,
    vernam_decrypt,
    generate_vernam_key,
    clean_key_alpha,
)
from utils import section_header, io_box

st.set_page_config(page_title="Vernam Cipher", layout="wide")

section_header(
    "Vernam Cipher (One-Time Pad)",
    "A theoretically unbreakable cipher -- if the key is truly random and used only once.",
)

with st.expander("Theory", expanded=True):
    st.markdown(
        """The **Vernam cipher**, invented by Gilbert Vernam in 1917, is the basis of
the **one-time pad (OTP)** -- the only encryption scheme mathematically
proven to be **perfectly secure**, provided three conditions are met:

1. The key is **truly random**.
2. The key is **at least as long as** the message.
3. The key is **used only once** and never reused.

It looks like a Vigenere cipher, but instead of a repeating keyword, it
uses a random key stream as long as the message itself, so patterns
never repeat. Originally implemented as an XOR of bits (for telegraph
signals), it's shown here as a mod-26 letter addition for clarity, which
is the same operation applied to letters instead of bits.
"""
    )

with st.expander("Procedure", expanded=False):
    st.markdown(
        """
**Encryption**
1. Generate a **random key** of letters at least as long as the plaintext
   (never reuse it for anything else).
2. For each plaintext letter `P` and the corresponding key letter `K`:
   `C = (P + K) mod 26`.
3. Non-alphabetic characters pass through unchanged.

**Decryption**
- `P = (C - K) mod 26`, using the *exact same* key.

Warning: If the key is reused across two messages, or isn't truly random, the
"perfect secrecy" guarantee is destroyed -- this is why real OTP systems
are hard to use safely (key distribution & storage is the weak point).
"""
    )

with st.expander("Worked Example", expanded=False):
    pt = "HELLO"
    random.seed(42)
    demo_key = generate_vernam_key(len(pt))
    rows = []
    for p, k in zip(pt, demo_key):
        xp = ord(p) - 65
        xk = ord(k) - 65
        c = (xp + xk) % 26
        rows.append(f"`{p}`({xp}) + `{k}`({xk}) = {xp+xk} mod 26 = {c} -> `{chr(c+65)}`")
    st.markdown(f"Plaintext: `{pt}`  |  Random key: `{demo_key}`")
    st.markdown("\n".join(f"- {r}" for r in rows))
    st.success(f"Ciphertext: `{vernam_encrypt(pt, demo_key)}`")

st.markdown("### Try It Yourself")
user_text = st.text_area("Enter text", "ATTACK AT DAWN", key="vernam_text")

if "vernam_key" not in st.session_state:
    st.session_state.vernam_key = ""

c1, c2 = st.columns([3, 1])
with c1:
    key_input = st.text_input(
        "Key (letters only, must be >= number of letters in text). Leave blank and click 'Generate Random Key'.",
        st.session_state.vernam_key,
        key="vernam_key_input",
    )
with c2:
    st.write("")
    st.write("")
    if st.button("Generate Random Key", key="vernam_gen"):
        n_letters = len([c for c in user_text if c.isalpha()])
        st.session_state.vernam_key = generate_vernam_key(max(n_letters, 1))
        st.rerun()

mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="vernam_mode")
if st.button("Run Vernam Cipher", key="vernam_run"):
    key_to_use = key_input if key_input else st.session_state.vernam_key
    key_to_use = clean_key_alpha(key_to_use)
    if not key_to_use:
        st.error("Please provide or generate a key first.")
    else:
        try:
            output = (
                vernam_encrypt(user_text, key_to_use)
                if mode == "Encrypt"
                else vernam_decrypt(user_text, key_to_use)
            )
            st.markdown(f"**Key used:** `{key_to_use}`")
            io_box("Input", "Output", user_text, output)
        except ValueError as e:
            st.error(str(e))