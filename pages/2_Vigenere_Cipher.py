import streamlit as st

from ciphers import vigenere_encrypt, vigenere_decrypt, clean_key_alpha
from utils import section_header, io_box

st.set_page_config(page_title="Vigenere Cipher", layout="wide")

section_header(
    "Vigenere Cipher",
    "A poly-alphabetic cipher that uses a repeating keyword to vary the shift.",
)

with st.expander("Theory", expanded=True):
    st.markdown(
        """The **Vigenere cipher**, described by Giovan Battista Bellaso in 1553 (later
misattributed to Blaise de Vigenere), improves on Caesar by using a
**keyword** instead of a single shift. Each letter of the keyword specifies
a different Caesar shift, so the same plaintext letter can map to different
ciphertext letters depending on its position -- this is called a
**poly-alphabetic substitution cipher**.

It was considered *"le chiffre indechiffrable"* (the indecipherable cipher)
for 300 years, until Charles Babbage and Friedrich Kasiski broke it in the
19th century by exploiting repeating patterns to guess the key length.
"""
    )

with st.expander("Procedure", expanded=False):
    st.markdown(
        """
**Encryption**
1. Choose a keyword, e.g. `KEY`.
2. Repeat the keyword to match the length of the plaintext
   (ignoring spaces/punctuation), e.g. plaintext `HELLO` -> key `KEYKE`.
3. For each plaintext letter `P` and corresponding key letter `K`:
   `C = (P + K) mod 26` (treating A=0 ... Z=25).
4. Non-alphabetic characters are left unchanged and don't consume a key letter.

**Decryption**
- `P = (C - K) mod 26`, using the same repeating keyword.
"""
    )

with st.expander("Worked Example", expanded=False):
    pt = "HELLO"
    key = "KEY"
    rep_key = "".join(key[i % len(key)] for i in range(len(pt)))
    st.markdown(f"Plaintext: `{pt}`  |  Keyword: `{key}` -> repeated key: `{rep_key}`")
    rows = []
    for p, k in zip(pt, rep_key):
        xp = ord(p) - 65
        xk = ord(k) - 65
        c = (xp + xk) % 26
        rows.append(f"`{p}`({xp}) + `{k}`({xk}) = {xp+xk} mod 26 = {c} -> `{chr(c+65)}`")
    st.markdown("\n".join(f"- {r}" for r in rows))
    st.success(f"Ciphertext: `{vigenere_encrypt(pt, key)}`")

st.markdown("### Try It Yourself")
c1, c2 = st.columns([2, 1])
with c1:
    user_text = st.text_area("Enter text", "ATTACK AT DAWN", key="vig_text")
with c2:
    key = st.text_input("Keyword", "LEMON", key="vig_key")
mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="vig_mode")
if st.button("Run Vigenere Cipher", key="vig_run"):
    if not clean_key_alpha(key):
        st.error("Please enter a valid alphabetic keyword.")
    else:
        output = vigenere_encrypt(user_text, key) if mode == "Encrypt" else vigenere_decrypt(user_text, key)
        io_box("Input", "Output", user_text, output)