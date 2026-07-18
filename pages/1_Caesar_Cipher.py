import streamlit as st

from ciphers import caesar_encrypt, caesar_decrypt
from utils import section_header, io_box

st.set_page_config(page_title="Caesar Cipher", layout="wide")

section_header(
    "Caesar Cipher",
    "The oldest known substitution cipher -- shift every letter by a fixed amount.",
)

with st.expander("Theory", expanded=True):
    st.markdown(
        """The **Caesar cipher** is one of the earliest and simplest encryption
techniques. It is named after **Julius Caesar**, who reportedly used it to
communicate with his generals. It is a **mono-alphabetic substitution
cipher**, meaning each letter in the plaintext is always replaced by the
*same* letter in the ciphertext.

Every letter of the alphabet is shifted a fixed number of positions
(the **key**, or *shift*). For example, with a shift of 3:

`A -> D, B -> E, C -> F, ... Z -> C`

Because there are only 26 possible shifts, this cipher is extremely weak
by modern standards -- it can be broken instantly by trying every shift
(**brute force**) or by **frequency analysis**.
"""
    )

with st.expander("Procedure", expanded=False):
    st.markdown(
        """
**Encryption**
1. Choose an integer key `k` (the shift), 0-25.
2. For each letter `P` in the plaintext, compute its position `x` in the
   alphabet (A = 0, B = 1, ... Z = 25).
3. Compute the new position: `C = (x + k) mod 26`.
4. Replace `P` with the letter at position `C`. Keep case and
   non-alphabetic characters unchanged.

**Decryption**
- Same process, but subtract the key: `P = (x - k) mod 26`.
"""
    )

with st.expander("Worked Example", expanded=False):
    example_text = "HELLO WORLD"
    example_shift = 3
    example_cipher = caesar_encrypt(example_text, example_shift)
    st.markdown(f"Plaintext: `{example_text}`  |  Shift key: `{example_shift}`")
    st.markdown("**Letter-by-letter walkthrough:**")
    rows = []
    for ch in example_text:
        if ch.isalpha():
            x = ord(ch) - 65
            c = (x + example_shift) % 26
            rows.append(f"`{ch}` (pos {x}) -> ({x}+{example_shift}) mod 26 = {c} -> `{chr(c+65)}`")
    st.markdown("\n".join(f"- {r}" for r in rows))
    st.success(f"Ciphertext: `{example_cipher}`")

st.markdown("### Try It Yourself")
c1, c2 = st.columns([2, 1])
with c1:
    user_text = st.text_area("Enter text", "ATTACK AT DAWN", key="caesar_text")
with c2:
    shift = st.slider("Shift key", 0, 25, 3, key="caesar_shift")
mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="caesar_mode")
if st.button("Run Caesar Cipher", key="caesar_run"):
    output = caesar_encrypt(user_text, shift) if mode == "Encrypt" else caesar_decrypt(user_text, shift)
    io_box("Input", "Output", user_text, output)