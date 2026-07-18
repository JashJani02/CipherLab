import streamlit as st

from ciphers import (
    hill_encrypt,
    hill_decrypt,
    matrix_det_2x2,
    mod_inverse,
    text_to_nums,
)
from utils import section_header, io_box

st.set_page_config(page_title="Hill Cipher", layout="wide")

section_header(
    "Hill Cipher",
    "A polygraphic cipher that uses matrix multiplication (linear algebra) to encrypt blocks of letters.",
)

with st.expander("Theory", expanded=True):
    st.markdown(
        """Invented by **Lester S. Hill** in 1929, the Hill cipher was the first
practical polygraphic substitution cipher based on **linear algebra**.
Instead of encrypting one letter at a time, it encrypts **blocks of `n`
letters at once** using an `n x n` key matrix, with all arithmetic done
modulo 26.

This app uses a **2x2 matrix**, so letters are encrypted in pairs
(digraphs). For the cipher to be decryptable, the key matrix must be
**invertible modulo 26** -- i.e. its determinant must be coprime with 26
(not divisible by 2 or 13).
"""
    )

with st.expander("Procedure", expanded=False):
    st.markdown(
        """
**Encryption**
1. Choose a 2x2 key matrix `K` whose determinant is coprime with 26.
2. Convert plaintext letters to numbers (A=0 ... Z=25); pad with `X` if
   the length is odd.
3. Split into pairs (vectors) `[p1, p2]`.
4. Multiply: `[c1, c2] = K x [p1, p2] mod 26`.
5. Convert the resulting numbers back to letters.

**Decryption**
1. Compute the modular inverse of the determinant of `K` mod 26.
2. Compute `K^-1` (the inverse matrix mod 26) using the adjugate matrix.
3. Multiply each ciphertext pair by `K^-1 mod 26` to recover the plaintext
   numbers, then convert back to letters.
"""
    )

with st.expander("Worked Example", expanded=False):
    key = [[3, 3], [2, 5]]
    pt = "HELP"
    st.markdown("Key matrix `K = [[3, 3], [2, 5]]` (det = 3x5 - 3x2 = 9 mod 26, coprime with 26)")
    st.markdown(f"Plaintext: `{pt}`")
    nums = text_to_nums(pt)
    st.markdown("Pairs (as numbers): " + ", ".join(f"({nums[i]},{nums[i+1]})" for i in range(0, len(nums), 2)))
    st.success(f"Ciphertext: `{hill_encrypt(pt, key)}`")
    st.markdown("Decrypting it back recovers the plaintext:")
    st.success(f"Decrypted: `{hill_decrypt(hill_encrypt(pt, key), key)}`")

st.markdown("### Try It Yourself")
user_text = st.text_area("Enter text (letters only)", "HELLO", key="hill_text")
st.markdown("**Key matrix (2x2):**")
k1, k2, k3, k4 = st.columns(4)
a = k1.number_input("K[0][0]", 0, 25, 3, key="hill_a")
b = k2.number_input("K[0][1]", 0, 25, 3, key="hill_b")
c = k3.number_input("K[1][0]", 0, 25, 2, key="hill_c")
d = k4.number_input("K[1][1]", 0, 25, 5, key="hill_d")
key_matrix = [[int(a), int(b)], [int(c), int(d)]]
det = matrix_det_2x2(key_matrix)
det_inv = mod_inverse(det, 26)
if det_inv is None:
    st.warning(f"Determinant = {det}, which is NOT invertible mod 26 (must be coprime with 26). Decryption won't be possible with this key.")
else:
    st.caption(f"Determinant = {det} (mod 26), modular inverse = {det_inv}. Key is valid.")

mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="hill_mode")
if st.button("Run Hill Cipher", key="hill_run"):
    try:
        output = hill_encrypt(user_text, key_matrix) if mode == "Encrypt" else hill_decrypt(user_text, key_matrix)
        io_box("Input", "Output", user_text, output)
    except ValueError as e:
        st.error(str(e))