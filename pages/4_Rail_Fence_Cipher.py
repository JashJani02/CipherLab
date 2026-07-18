import streamlit as st

from ciphers import rail_fence_encrypt, rail_fence_decrypt, rail_fence_grid
from utils import section_header, io_box

st.set_page_config(page_title="Rail Fence Cipher", layout="wide")

section_header(
    "Rail Fence Cipher",
    "A transposition cipher that rearranges letters in a zig-zag pattern.",
)

with st.expander("Theory", expanded=True):
    st.markdown(
        """Unlike substitution ciphers, the **Rail Fence cipher** doesn't change any
letters -- it only **rearranges** their order (a **transposition
cipher**). The plaintext is written in a zig-zag pattern across a number
of "rails" (rows), then read off row by row to produce the ciphertext.

It's easy to visualize and simple to break with short messages, since
the number of rails is a small, guessable key (brute-forceable).
"""
    )

with st.expander("Procedure", expanded=False):
    st.markdown(
        """
**Encryption**
1. Choose the number of rails `r`.
2. Write the plaintext diagonally, moving down each rail, then back up
   once you hit the bottom rail, then back down again -- a zig-zag.
3. Read the letters off **row by row** to get the ciphertext.

**Decryption**
1. Figure out the zig-zag pattern of positions for the given rail count
   and ciphertext length.
2. Count how many letters fall on each rail.
3. Slice the ciphertext into those rail-sized chunks and lay them back
   into their zig-zag positions.
4. Read the letters off in original (row-then-column zig-zag) order.
"""
    )

with st.expander("Worked Example", expanded=False):
    pt = "WEAREDISCOVERED"
    rails = 3
    grid = rail_fence_grid(pt, rails)
    st.markdown(f"Plaintext: `{pt}`  |  Rails: `{rails}`")
    st.markdown("**Zig-zag grid:**")
    st.table(grid)
    st.success(f"Ciphertext (read row by row): `{rail_fence_encrypt(pt, rails)}`")

st.markdown("### Try It Yourself")
c1, c2 = st.columns([2, 1])
with c1:
    user_text = st.text_area("Enter text (letters recommended)", "DEFEND THE EAST WALL", key="rf_text")
with c2:
    rails = st.slider("Number of rails", 2, 10, 3, key="rf_rails")
mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="rf_mode")
if st.button("Run Rail Fence Cipher", key="rf_run"):
    clean_text = user_text.replace(" ", "")
    if mode == "Encrypt":
        output = rail_fence_encrypt(clean_text, rails)
        grid = rail_fence_grid(clean_text, rails)
        st.markdown("**Zig-zag pattern used:**")
        st.table(grid)
    else:
        output = rail_fence_decrypt(clean_text, rails)
    io_box("Input (spaces removed)", "Output", clean_text, output)