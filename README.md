# 🔐 CipherLab

A modular Streamlit-based educational application for classical cryptography. Provides six dedicated interfaces, Caesar, Vigenère, Vernam, Rail Fence, Hill, and Playfair. Each covering theory, step-by-step procedure, a worked example, and a live encrypt/decrypt playground, all powered by a shared `ciphers.py` logic core.

---

## Project Structure

```
CipherLab/
│
├── app.py                          # Main entry point (Home page)
├── README.md                       # README file
├── requirements.txt                # Python dependencies
│
├── ciphers.py                      # All cipher algorithms (encrypt/decrypt logic, framework-agnostic)
├── utils.py                        # Shared Streamlit UI helper components
│
└── pages/
    ├── 1_Caesar_Cipher.py          # Mono-alphabetic shift cipher
    ├── 2_Vigenere_Cipher.py        # Poly-alphabetic keyword cipher
    ├── 3_Vernam_Cipher.py          # One-time pad cipher
    ├── 4_Rail_Fence_Cipher.py      # Zig-zag transposition cipher
    ├── 5_Hill_Cipher.py            # Matrix-based polygraphic cipher
    └── 6_Playfair_Cipher.py        # Digraph substitution cipher
```

---

## Requirements & Setup

- **Python:** 3.9+
- **Dependencies:** `streamlit` 

```bash
pip install -r requirements.txt
streamlit run app.py
```

> Streamlit auto-discovers every file inside `pages/` and builds the sidebar navigation from the filenames. The numeric prefixes (`1_`, `2_`, ...) control display order and are stripped from the visible page name.

---

## Pages

### 1. `1_Caesar_Cipher.py` — Caesar Cipher

| Section | What It Covers |
|---|---|
| Theory | History of the mono-alphabetic shift cipher and why it's trivially breakable (brute force / frequency analysis) |
| Procedure | Encryption/decryption steps: `C = (x + k) mod 26` and its inverse |
| Worked Example | Letter-by-letter walkthrough of `"HELLO WORLD"` shifted by 3 |
| Try It Yourself | Free-text input, shift slider (0–25), Encrypt/Decrypt toggle |

### 2. `2_Vigenere_Cipher.py` — Vigenère Cipher

| Section | What It Covers |
|---|---|
| Theory | Poly-alphabetic substitution using a repeating keyword; historical note on Babbage/Kasiski breaking it |
| Procedure | Key repetition to match plaintext length, then `C = (P + K) mod 26` per letter |
| Worked Example | Keyword `"KEY"` applied to `"HELLO"` with a full addition breakdown |
| Try It Yourself | Free-text input, keyword field, Encrypt/Decrypt toggle |

### 3. `3_Vernam_Cipher.py` — Vernam Cipher (One-Time Pad)

| Section | What It Covers |
|---|---|
| Theory | Perfect secrecy conditions (truly random, key ≥ message length, single use) |
| Procedure | Random key generation and mod-26 addition/subtraction, with a warning on key reuse |
| Worked Example | Seeded random key applied to `"HELLO"` |
| Try It Yourself | Free-text input, manual key entry or one-click random key generation, Encrypt/Decrypt toggle |

### 4. `4_Rail_Fence_Cipher.py` — Rail Fence Cipher

| Section | What It Covers |
|---|---|
| Theory | Transposition (not substitution) cipher — letters are reordered, not replaced |
| Procedure | Zig-zag writing across `r` rails, then row-by-row reading |
| Worked Example | 3-rail zig-zag of `"WEAREDISCOVERED"`, rendered as a visual grid |
| Try It Yourself | Free-text input, rail-count slider (2–10), live zig-zag grid preview, Encrypt/Decrypt toggle |

### 5. `5_Hill_Cipher.py` — Hill Cipher

| Section | What It Covers |
|---|---|
| Theory | Polygraphic substitution via 2×2 matrix multiplication mod 26; invertibility requirement |
| Procedure | Letter-pair vectors multiplied by the key matrix; inverse matrix via adjugate method for decryption |
| Worked Example | Key matrix `[[3,3],[2,5]]` applied to `"HELP"`, with round-trip decryption shown |
| Try It Yourself | Free-text input, 4 numeric fields for the 2×2 key matrix, live determinant/invertibility check, Encrypt/Decrypt toggle |

### 6. `6_Playfair_Cipher.py` — Playfair Cipher

| Section | What It Covers |
|---|---|
| Theory | First digraph substitution cipher; 5×5 key grid construction (I/J merged) |
| Procedure | Digraph preparation rules (padding, repeated-letter handling) and row/column/rectangle encryption rules |
| Worked Example | Keyword `"MONARCHY"` grid applied to `"INSTRUMENTS"` |
| Try It Yourself | Keyword field with live 5×5 grid preview, free-text input, Encrypt/Decrypt toggle |

---

## `ciphers.py` — Cipher Logic Core

Pure Python module with no Streamlit dependency, every function is framework-agnostic and independently testable.

### Caesar Cipher

| Function | Description |
|---|---|
| `caesar_encrypt(text, shift)` | Shifts each alphabetic character forward by `shift` positions (mod 26); case and non-alphabetic characters preserved |
| `caesar_decrypt(text, shift)` | Reverses `caesar_encrypt` by calling it internally with `-shift` |

### Vigenère Cipher

| Function | Description |
|---|---|
| `clean_key_alpha(key)` | Strips non-alphabetic characters and uppercases `key`; shared helper also used by Vernam and Playfair |
| `vigenere_encrypt(text, key)` | Encrypts using a repeating-keyword poly-alphabetic shift; non-alphabetic characters pass through without consuming a key letter |
| `vigenere_decrypt(text, key)` | Reverses `vigenere_encrypt` using the same keyword |

### Vernam Cipher (One-Time Pad)

| Function | Description |
|---|---|
| `generate_vernam_key(length)` | Generates a random uppercase key of the given `length` via `random.choice` |
| `vernam_encrypt(text, key)` | Adds each plaintext letter to the corresponding key letter (mod 26); raises `ValueError` if `key` is too short |
| `vernam_decrypt(text, key)` | Reverses `vernam_encrypt` using the same key (subtraction mod 26); same length validation |

### Rail Fence Cipher

| Function | Description |
|---|---|
| `rail_fence_pattern(length, rails)` | Computes the zig-zag rail index for each position; internal helper shared by encrypt, decrypt, and grid functions |
| `rail_fence_encrypt(text, rails)` | Writes `text` in a zig-zag across `rails` rows, then reads it back row by row |
| `rail_fence_decrypt(cipher, rails)` | Reconstructs the zig-zag layout from rail counts and reassembles the original order |
| `rail_fence_grid(text, rails)` | Builds a 2D visual grid (`.` for empty cells) representing the zig-zag pattern, used for the UI diagram |

### Hill Cipher (2×2)

| Function | Description |
|---|---|
| `mod_inverse(a, m)` | Brute-force search for the modular multiplicative inverse of `a` mod `m`; returns `None` if it doesn't exist |
| `matrix_det_2x2(mat)` | Computes the determinant of a 2×2 matrix, mod 26 |
| `matrix_inverse_2x2(mat)` | Computes the mod-26 inverse of a 2×2 matrix via the adjugate method; returns `None` if not invertible |
| `text_to_nums(text)` | Converts alphabetic characters to 0–25 numeric values (A=0 ... Z=25), ignoring non-alphabetic characters |
| `nums_to_text(nums)` | Converts a list of 0–25 integers back into uppercase letters |
| `hill_encrypt(text, key_matrix)` | Encrypts `text` in letter-pairs via matrix multiplication with `key_matrix`, mod 26; pads with `X` if the letter count is odd |
| `hill_decrypt(text, key_matrix)` | Decrypts using the inverse of `key_matrix`; raises `ValueError` if the matrix isn't invertible mod 26 |

### Playfair Cipher

| Function | Description |
|---|---|
| `playfair_generate_grid(key)` | Builds the 5×5 Playfair key square from `key` (merges I/J, removes duplicates, fills remaining alphabet in order) |
| `_find_pos(grid, ch)` | Internal helper — locates the `(row, col)` position of a character within the grid |
| `playfair_prepare_text(text)` | Prepares plaintext into valid digraphs: inserts `X` between repeated letters in a pair and pads a trailing single letter |
| `playfair_encrypt(text, key)` | Encrypts using the Playfair row/column/rectangle substitution rules |
| `playfair_decrypt(text, key)` | Reverses `playfair_encrypt` using the same keyword |

---

## `utils.py` — Shared UI Components

Small Streamlit-specific helper components reused across every page.

| Function | Description |
|---|---|
| `section_header(title, subtitle)` | Renders a page-level `##` heading, a caption subtitle, and a divider — used at the top of every cipher page |
| `io_box(label_left, label_right, left_val, right_val)` | Renders a two-column comparison box (e.g. "Input" vs "Output") using `st.code` blocks |

---

## `app.py` — Entry Point

Configures the app (`st.set_page_config`) and renders the Home page — a static overview with no cipher logic of its own.

| Section | Content |
|---|---|
| Page config | Title `"Classical Cryptography Lab"`, wide layout, expanded sidebar |
| Overview table | All 6 ciphers compared by type, key, unit encrypted, and era |
| How to use | Numbered instructions for navigating the app |
| Tip callout | `st.info()` note on the real-world security limitations of classical ciphers |

---

## Architecture Notes

- **Separation of Concerns:** `ciphers.py` contains zero Streamlit imports — every cipher function is a pure function of its inputs, so the cryptographic logic can be unit-tested or reused entirely outside the app.
- **No Duplication:** every page imports shared cipher logic from `ciphers.py` and shared UI patterns (`section_header`, `io_box`) from `utils.py` instead of redefining them inline.
- **Mod-26 Arithmetic Consistency:** all substitution ciphers (Caesar, Vigenère, Vernam, Hill) share the same `(value ± key) mod 26` pattern, keeping encrypt/decrypt symmetric and easy to reason about.
- **Convention-Based Routing:** Streamlit's native `pages/` directory auto-generates the sidebar; numeric filename prefixes (`1_`, `2_`, ...) control ordering without any manual navigation code.
- **State Management:** the Vernam page uses `st.session_state["vernam_key"]` to persist a randomly generated key across reruns, so it survives Streamlit's rerun-on-interaction model.
- **Error Resilience:** functions that can fail on invalid input (`vernam_encrypt`/`decrypt` on a too-short key, `hill_decrypt` on a non-invertible matrix) raise `ValueError` with a descriptive message, which each page catches and surfaces via `st.error()`.
- **Live Validation:** the Hill Cipher page recomputes the determinant and modular inverse on every rerun and warns the user immediately if their chosen key matrix isn't invertible mod 26, before they attempt to decrypt anything.

---

## Notes on Security

These are **classical/historical ciphers** intended for learning purposes only. None of them (except a correctly used one-time pad) are secure by modern standards, they're all vulnerable to frequency analysis, brute force, or known-plaintext attacks. Do not use this app to protect real sensitive data.

---

## License & Credits

Built for educational purposes to learn and understand traditional cryptographic techniques. No external data dependencies, all cipher logic is implemented from first principles using the Python standard library.