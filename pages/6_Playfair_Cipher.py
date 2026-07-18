import streamlit as st

from ciphers import (
    playfair_encrypt,
    playfair_decrypt,
    playfair_generate_grid,
    playfair_prepare_text,
    clean_key_alpha,
)
from utils import section_header, io_box

st.set_page_config(page_title="Playfair Cipher", layout="wide")

section_header(
    "Playfair Cipher",
    "A digraph substitution cipher that encrypts letters in pairs using a 5x5 key grid.",
)

with st.expander("Theory", expanded=True):
    st.markdown(
        """Invented by **Charles Wheatstone** in 1854 (popularized by Lord Playfair),
this was the first cipher to encrypt **pairs of letters (digraphs)**
instead of single letters, making simple frequency analysis much harder.

A keyword is used to build a **5x5 grid** of the alphabet (I and J share
a cell). The plaintext is split into letter pairs and encrypted based on
the pair's position **relative to each other** in the grid.
"""
    )

with st.expander("Procedure", expanded=False):
    st.markdown(
        """
**Building the grid**
1. Write the keyword into the grid, removing duplicate letters, and
   merging I/J into a single cell.
2. Fill the rest of the grid with the remaining letters of the alphabet
   in order.

**Preparing the plaintext**
1. Split the plaintext into pairs of letters.
2. If a pair has two identical letters, insert an `X` between them.
3. If the final pair has only one letter, pad it with an `X`.

**Encrypting each pair (A, B)**
- **Same row:** replace each letter with the one to its **right**
  (wrapping around).
- **Same column:** replace each letter with the one **below** it
  (wrapping around).
- **Rectangle (different row & column):** replace each letter with the
  one in its own row but in the **other letter's column**.

**Decryption** reverses the same three rules (left instead of right,
above instead of below).
"""
    )

with st.expander("Worked Example", expanded=False):
    key = "MONARCHY"
    grid = playfair_generate_grid(key)
    st.markdown(f"Keyword: `{key}`")
    st.markdown("**5x5 grid:**")
    st.table(grid)
    pt = "INSTRUMENTS"
    prepared = playfair_prepare_text(pt)
    st.markdown(f"Plaintext: `{pt}` -> prepared into pairs: `{' '.join(prepared[i:i+2] for i in range(0, len(prepared), 2))}`")
    st.success(f"Ciphertext: `{playfair_encrypt(pt, key)}`")

st.markdown("### Try It Yourself")
key = st.text_input("Keyword", "MONARCHY", key="pf_key")
if key.strip():
    st.markdown("**Generated 5x5 grid:**")
    st.table(playfair_generate_grid(key))
user_text = st.text_area("Enter text (letters only)", "INSTRUMENTS", key="pf_text")
mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="pf_mode")
if st.button("Run Playfair Cipher", key="pf_run"):
    if not clean_key_alpha(key):
        st.error("Please enter a valid alphabetic keyword.")
    else:
        output = playfair_encrypt(user_text, key) if mode == "Encrypt" else playfair_decrypt(user_text, key)
        io_box("Input", "Output", user_text, output)