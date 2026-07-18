import streamlit as st

st.set_page_config(
    page_title="Classical Cryptography Lab",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("# Classical Cryptography Lab")
st.markdown(
    "Welcome! This is an interactive playground for learning six classic "
    "encryption techniques -- from the simple **Caesar shift** to the "
    "matrix-based **Hill cipher**. Pick a cipher from the sidebar to see "
    "its history, step-by-step procedure, a worked example, and a live "
    "encrypt/decrypt tool you can experiment with."
)

st.markdown("### Overview")
st.markdown(
    """
| Cipher | Type | Key | Unit Encrypted | Era |
|---|---|---|---|---|
| Caesar | Substitution (mono-alphabetic) | Single number (shift) | 1 letter | ~100 BC (Julius Caesar) |
| Vigenere | Substitution (poly-alphabetic) | Word/phrase | 1 letter | 1553 (Giovan Bellaso) |
| Vernam | Substitution (one-time pad) | Random key >= message length | 1 letter/bit | 1917 (Gilbert Vernam) |
| Rail Fence | Transposition | Number of rails | Whole message | Ancient (Spartan-era idea) |
| Hill | Substitution (polygraphic, linear algebra) | n x n matrix | n letters (block) | 1929 (Lester Hill) |
| Playfair | Substitution (digraph) | Keyword (5x5 grid) | 2 letters (pair) | 1854 (Charles Wheatstone) |
"""
)

st.markdown("### How to use this app")
st.markdown(
    """
1. Choose a cipher from the **sidebar**.
2. Read the **Theory** and **Procedure** to understand how it works.
3. Walk through the **Worked Example** to see it applied step by step.
4. Head to **Try It Yourself** to encrypt or decrypt your own text.
"""
)

st.info(
    "Tip: Classical ciphers are great for learning cryptographic "
    "concepts, but none of them are secure by modern standards (except "
    "a *correctly used* one-time pad / Vernam cipher, which is "
    "mathematically unbreakable but impractical to use safely)."
)