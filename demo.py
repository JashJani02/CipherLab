import streamlit as st
import random
import string
import math

# =========================================================================
# PAGE CONFIG
# =========================================================================
st.set_page_config(
    page_title="Classical Cryptography Lab",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================================
# ---------------------------  CIPHER LOGIC  -----------------------------
# =========================================================================

# ---------- 1. Caesar Cipher ----------
def caesar_encrypt(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# ---------- 2. Vigenere Cipher ----------
def _clean_key_alpha(key):
    return "".join(ch for ch in key.upper() if ch.isalpha())


def vigenere_encrypt(text, key):
    key = _clean_key_alpha(key)
    if not key:
        return text
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            shift = ord(key[ki % len(key)]) - 65
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)


def vigenere_decrypt(text, key):
    key = _clean_key_alpha(key)
    if not key:
        return text
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            shift = ord(key[ki % len(key)]) - 65
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)


# ---------- 3. Vernam Cipher (One-Time Pad, mod-26 letters) ----------
def generate_vernam_key(length):
    return "".join(random.choice(string.ascii_uppercase) for _ in range(length))


def vernam_encrypt(text, key):
    letters_only = [ch for ch in text if ch.isalpha()]
    if len(key) < len(letters_only):
        raise ValueError("Key must be at least as long as the number of letters in the plaintext.")
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            k = ord(key[ki].upper()) - 65
            result.append(chr((ord(ch.upper()) - 65 + k) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)


def vernam_decrypt(text, key):
    letters_only = [ch for ch in text if ch.isalpha()]
    if len(key) < len(letters_only):
        raise ValueError("Key must be at least as long as the number of letters in the ciphertext.")
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            k = ord(key[ki].upper()) - 65
            result.append(chr((ord(ch.upper()) - 65 - k) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)


# ---------- 4. Rail Fence Cipher ----------
def rail_fence_pattern(length, rails):
    pattern = []
    rail = 0
    direction = 1
    for _ in range(length):
        pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
    return pattern


def rail_fence_encrypt(text, rails):
    if rails < 2:
        return text
    pattern = rail_fence_pattern(len(text), rails)
    fence = [[] for _ in range(rails)]
    for ch, r in zip(text, pattern):
        fence[r].append(ch)
    return "".join("".join(row) for row in fence)


def rail_fence_decrypt(cipher, rails):
    if rails < 2:
        return cipher
    pattern = rail_fence_pattern(len(cipher), rails)
    counts = [pattern.count(r) for r in range(rails)]
    rows = []
    idx = 0
    for c in counts:
        rows.append(list(cipher[idx: idx + c]))
        idx += c
    pointers = [0] * rails
    result = []
    for r in pattern:
        result.append(rows[r][pointers[r]])
        pointers[r] += 1
    return "".join(result)


def rail_fence_grid(text, rails):
    """Return a visual grid (list of lists) with '.' for empty spots."""
    pattern = rail_fence_pattern(len(text), rails)
    grid = [["." for _ in range(len(text))] for _ in range(rails)]
    for col, (ch, r) in enumerate(zip(text, pattern)):
        grid[r][col] = ch
    return grid


# ---------- 5. Hill Cipher (2x2) ----------
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def matrix_det_2x2(mat):
    return (mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]) % 26


def matrix_inverse_2x2(mat):
    det = matrix_det_2x2(mat)
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        return None
    a, b = mat[0]
    c, d = mat[1]
    inv = [
        [(d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, (a * det_inv) % 26],
    ]
    return inv


def _text_to_nums(text):
    return [ord(c.upper()) - 65 for c in text if c.isalpha()]


def _nums_to_text(nums):
    return "".join(chr(n % 26 + 65) for n in nums)


def hill_encrypt(text, key_matrix):
    nums = _text_to_nums(text)
    if len(nums) % 2 != 0:
        nums.append(ord("X") - 65)  # pad
    cipher_nums = []
    for i in range(0, len(nums), 2):
        p1, p2 = nums[i], nums[i + 1]
        c1 = (key_matrix[0][0] * p1 + key_matrix[0][1] * p2) % 26
        c2 = (key_matrix[1][0] * p1 + key_matrix[1][1] * p2) % 26
        cipher_nums.extend([c1, c2])
    return _nums_to_text(cipher_nums)


def hill_decrypt(text, key_matrix):
    inv = matrix_inverse_2x2(key_matrix)
    if inv is None:
        raise ValueError("Key matrix is not invertible mod 26. Choose a different key.")
    nums = _text_to_nums(text)
    plain_nums = []
    for i in range(0, len(nums), 2):
        c1, c2 = nums[i], nums[i + 1]
        p1 = (inv[0][0] * c1 + inv[0][1] * c2) % 26
        p2 = (inv[1][0] * c1 + inv[1][1] * c2) % 26
        plain_nums.extend([p1, p2])
    return _nums_to_text(plain_nums)


# ---------- 6. Playfair Cipher ----------
def playfair_generate_grid(key):
    key = "".join(ch for ch in key.upper() if ch.isalpha()).replace("J", "I")
    seen = []
    for ch in key:
        if ch not in seen:
            seen.append(ch)
    for ch in string.ascii_uppercase:
        if ch == "J":
            continue
        if ch not in seen:
            seen.append(ch)
    grid = [seen[i * 5:(i + 1) * 5] for i in range(5)]
    return grid


def _find_pos(grid, ch):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == ch:
                return r, c
    return None


def playfair_prepare_text(text):
    letters = [ch.upper() for ch in text if ch.isalpha()]
    letters = ["I" if ch == "J" else ch for ch in letters]
    prepared = []
    i = 0
    while i < len(letters):
        a = letters[i]
        b = letters[i + 1] if i + 1 < len(letters) else None
        if b is None:
            prepared.append(a)
            prepared.append("X")
            i += 1
        elif a == b:
            prepared.append(a)
            prepared.append("X")
            i += 1
        else:
            prepared.append(a)
            prepared.append(b)
            i += 2
    if len(prepared) % 2 != 0:
        prepared.append("X")
    return "".join(prepared)


def playfair_encrypt(text, key):
    grid = playfair_generate_grid(key)
    prepared = playfair_prepare_text(text)
    result = []
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i + 1]
        ra, ca = _find_pos(grid, a)
        rb, cb = _find_pos(grid, b)
        if ra == rb:
            result.append(grid[ra][(ca + 1) % 5])
            result.append(grid[rb][(cb + 1) % 5])
        elif ca == cb:
            result.append(grid[(ra + 1) % 5][ca])
            result.append(grid[(rb + 1) % 5][cb])
        else:
            result.append(grid[ra][cb])
            result.append(grid[rb][ca])
    return "".join(result)


def playfair_decrypt(text, key):
    grid = playfair_generate_grid(key)
    text = "".join(ch.upper() for ch in text if ch.isalpha())
    result = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        ra, ca = _find_pos(grid, a)
        rb, cb = _find_pos(grid, b)
        if ra == rb:
            result.append(grid[ra][(ca - 1) % 5])
            result.append(grid[rb][(cb - 1) % 5])
        elif ca == cb:
            result.append(grid[(ra - 1) % 5][ca])
            result.append(grid[(rb - 1) % 5][cb])
        else:
            result.append(grid[ra][cb])
            result.append(grid[rb][ca])
    return "".join(result)


# =========================================================================
# ---------------------------  UI HELPERS  --------------------------------
# =========================================================================

def section_header(title, subtitle):
    st.markdown(f"## {title}")
    st.caption(subtitle)
    st.divider()


def io_box(label_left, label_right, left_val, right_val):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{label_left}**")
        st.code(left_val if left_val else " ", language=None)
    with c2:
        st.markdown(f"**{label_right}**")
        st.code(right_val if right_val else " ", language=None)


# =========================================================================
# ---------------------------  PAGES  --------------------------------------
# =========================================================================

def home_page():
    st.markdown("# Classical Cryptography Lab")
    st.markdown(
        "Welcome! This is an interactive playground for learning six classic "
        "encryption techniques — from the simple **Caesar shift** to the "
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
| Vigenère | Substitution (poly-alphabetic) | Word/phrase | 1 letter | 1553 (Giovan Bellaso) |
| Vernam | Substitution (one-time pad) | Random key ≥ message length | 1 letter/bit | 1917 (Gilbert Vernam) |
| Rail Fence | Transposition | Number of rails | Whole message | Ancient (Spartan-era idea) |
| Hill | Substitution (polygraphic, linear algebra) | n×n matrix | n letters (block) | 1929 (Lester Hill) |
| Playfair | Substitution (digraph) | Keyword (5×5 grid) | 2 letters (pair) | 1854 (Charles Wheatstone) |
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


# ---------------- CAESAR PAGE ----------------
def caesar_page():
    section_header("Caesar Cipher", "The oldest known substitution cipher — shift every letter by a fixed amount.")

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
by modern standards — it can be broken instantly by trying every shift
(**brute force**) or by **frequency analysis**.
"""
        )

    with st.expander("Procedure", expanded=False):
        st.markdown(
            """
**Encryption**
1. Choose an integer key `k` (the shift), 0–25.
2. For each letter `P` in the plaintext, compute its position `x` in the
   alphabet (A = 0, B = 1, ... Z = 25).
3. Compute the new position: `C = (x + k) mod 26`.
4. Replace `P` with the letter at position `C`. Keep case and
   non-alphabetic characters unchanged.

**Decryption**
- Same process, but subtract the key: `P = (x − k) mod 26`.
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


# ---------------- VIGENERE PAGE ----------------
def vigenere_page():
    section_header("Vigenère Cipher", "A poly-alphabetic cipher that uses a repeating keyword to vary the shift.")

    with st.expander("Theory", expanded=True):
        st.markdown(
            """The **Vigenère cipher**, described by Giovan Battista Bellaso in 1553 (later
misattributed to Blaise de Vigenère), improves on Caesar by using a
**keyword** instead of a single shift. Each letter of the keyword specifies
a different Caesar shift, so the same plaintext letter can map to different
ciphertext letters depending on its position — this is called a
**poly-alphabetic substitution cipher**.

It was considered *"le chiffre indéchiffrable"* (the indecipherable cipher)
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
- `P = (C − K) mod 26`, using the same repeating keyword.
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
    if st.button("Run Vigenère Cipher", key="vig_run"):
        if not _clean_key_alpha(key):
            st.error("Please enter a valid alphabetic keyword.")
        else:
            output = vigenere_encrypt(user_text, key) if mode == "Encrypt" else vigenere_decrypt(user_text, key)
            io_box("Input", "Output", user_text, output)


# ---------------- VERNAM PAGE ----------------
def vernam_page():
    section_header("Vernam Cipher (One-Time Pad)", "A theoretically unbreakable cipher — if the key is truly random and used only once.")

    with st.expander("Theory", expanded=True):
        st.markdown(
            """The **Vernam cipher**, invented by Gilbert Vernam in 1917, is the basis of
the **one-time pad (OTP)** — the only encryption scheme mathematically
proven to be **perfectly secure**, provided three conditions are met:

1. The key is **truly random**.
2. The key is **at least as long as** the message.
3. The key is **used only once** and never reused.

It looks like a Vigenère cipher, but instead of a repeating keyword, it
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
- `P = (C − K) mod 26`, using the *exact same* key.

 If the key is reused across two messages, or isn't truly random, the
"perfect secrecy" guarantee is destroyed — this is why real OTP systems
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
            "Key (letters only, must be ≥ number of letters in text). Leave blank and click 'Generate Random Key'.",
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
        key_to_use = _clean_key_alpha(key_to_use)
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


# ---------------- RAIL FENCE PAGE ----------------
def railfence_page():
    section_header("Rail Fence Cipher", "A transposition cipher that rearranges letters in a zig-zag pattern.")

    with st.expander("Theory", expanded=True):
        st.markdown(
            """Unlike substitution ciphers, the **Rail Fence cipher** doesn't change any
letters — it only **rearranges** their order (a **transposition
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
   once you hit the bottom rail, then back down again — a zig-zag.
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


# ---------------- HILL PAGE ----------------
def hill_page():
    section_header("Hill Cipher", "A polygraphic cipher that uses matrix multiplication (linear algebra) to encrypt blocks of letters.")

    with st.expander("Theory", expanded=True):
        st.markdown(
            """Invented by **Lester S. Hill** in 1929, the Hill cipher was the first
practical polygraphic substitution cipher based on **linear algebra**.
Instead of encrypting one letter at a time, it encrypts **blocks of `n`
letters at once** using an `n × n` key matrix, with all arithmetic done
modulo 26.

This app uses a **2×2 matrix**, so letters are encrypted in pairs
(digraphs). For the cipher to be decryptable, the key matrix must be
**invertible modulo 26** — i.e. its determinant must be coprime with 26
(not divisible by 2 or 13).
"""
        )

    with st.expander("Procedure", expanded=False):
        st.markdown(
            """
**Encryption**
1. Choose a 2×2 key matrix `K` whose determinant is coprime with 26.
2. Convert plaintext letters to numbers (A=0 ... Z=25); pad with `X` if
   the length is odd.
3. Split into pairs (vectors) `[p1, p2]`.
4. Multiply: `[c1, c2] = K × [p1, p2] mod 26`.
5. Convert the resulting numbers back to letters.

**Decryption**
1. Compute the modular inverse of the determinant of `K` mod 26.
2. Compute `K⁻¹` (the inverse matrix mod 26) using the adjugate matrix.
3. Multiply each ciphertext pair by `K⁻¹ mod 26` to recover the plaintext
   numbers, then convert back to letters.
"""
        )

    with st.expander("Worked Example", expanded=False):
        key = [[3, 3], [2, 5]]
        pt = "HELP"
        st.markdown("Key matrix `K = [[3, 3], [2, 5]]` (det = 3×5 − 3×2 = 9 mod 26, coprime with 26)")
        st.markdown(f"Plaintext: `{pt}`")
        nums = _text_to_nums(pt)
        st.markdown("Pairs (as numbers): " + ", ".join(f"({nums[i]},{nums[i+1]})" for i in range(0, len(nums), 2)))
        st.success(f"Ciphertext: `{hill_encrypt(pt, key)}`")
        st.markdown("Decrypting it back recovers the plaintext:")
        st.success(f"Decrypted: `{hill_decrypt(hill_encrypt(pt, key), key)}`")

    st.markdown("### Try It Yourself")
    user_text = st.text_area("Enter text (letters only)", "HELLO", key="hill_text")
    st.markdown("**Key matrix (2×2):**")
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


# ---------------- PLAYFAIR PAGE ----------------
def playfair_page():
    section_header("Playfair Cipher", "A digraph substitution cipher that encrypts letters in pairs using a 5×5 key grid.")

    with st.expander("Theory", expanded=True):
        st.markdown(
            """Invented by **Charles Wheatstone** in 1854 (popularized by Lord Playfair),
this was the first cipher to encrypt **pairs of letters (digraphs)**
instead of single letters, making simple frequency analysis much harder.

A keyword is used to build a **5×5 grid** of the alphabet (I and J share
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
        st.markdown("**5×5 grid:**")
        st.table(grid)
        pt = "INSTRUMENTS"
        prepared = playfair_prepare_text(pt)
        st.markdown(f"Plaintext: `{pt}` -> prepared into pairs: `{' '.join(prepared[i:i+2] for i in range(0, len(prepared), 2))}`")
        st.success(f"Ciphertext: `{playfair_encrypt(pt, key)}`")

    st.markdown("### Try It Yourself")
    key = st.text_input("Keyword", "MONARCHY", key="pf_key")
    if key.strip():
        st.markdown("**Generated 5×5 grid:**")
        st.table(playfair_generate_grid(key))
    user_text = st.text_area("Enter text (letters only)", "INSTRUMENTS", key="pf_text")
    mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="pf_mode")
    if st.button("Run Playfair Cipher", key="pf_run"):
        if not _clean_key_alpha(key):
            st.error("Please enter a valid alphabetic keyword.")
        else:
            output = playfair_encrypt(user_text, key) if mode == "Encrypt" else playfair_decrypt(user_text, key)
            io_box("Input", "Output", user_text, output)


# =========================================================================
# ---------------------------  NAVIGATION  ---------------------------------
# =========================================================================

PAGES = {
    "Home": home_page,
    "Caesar Cipher": caesar_page,
    "Vigenère Cipher": vigenere_page,
    "Vernam Cipher": vernam_page,
    "Rail Fence Cipher": railfence_page,
    "Hill Cipher": hill_page,
    "Playfair Cipher": playfair_page,
}

st.sidebar.title("Crypto Lab")
st.sidebar.caption("Learn classical encryption, step by step.")
choice = st.sidebar.selectbox("Select a cipher", list(PAGES.keys()))
st.sidebar.divider()
st.sidebar.markdown(
    "Built as a hands-on companion for learning six classic ciphers: "
    "Caesar, Vigenère, Vernam, Rail Fence, Hill, and Playfair."
)

PAGES[choice]()