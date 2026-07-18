"""
Shared cipher implementations used by every page of the Classical
Cryptography Lab app. Kept separate from the Streamlit UI code so the
logic can be tested and reused independently.
"""

import random
import string

# =========================================================================
# 1. Caesar Cipher
# =========================================================================
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


# =========================================================================
# 2. Vigenere Cipher
# =========================================================================
def clean_key_alpha(key):
    return "".join(ch for ch in key.upper() if ch.isalpha())


def vigenere_encrypt(text, key):
    key = clean_key_alpha(key)
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
    key = clean_key_alpha(key)
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


# =========================================================================
# 3. Vernam Cipher (One-Time Pad, mod-26 letters)
# =========================================================================
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


# =========================================================================
# 4. Rail Fence Cipher
# =========================================================================
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


# =========================================================================
# 5. Hill Cipher (2x2)
# =========================================================================
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


def text_to_nums(text):
    return [ord(c.upper()) - 65 for c in text if c.isalpha()]


def nums_to_text(nums):
    return "".join(chr(n % 26 + 65) for n in nums)


def hill_encrypt(text, key_matrix):
    nums = text_to_nums(text)
    if len(nums) % 2 != 0:
        nums.append(ord("X") - 65)  # pad
    cipher_nums = []
    for i in range(0, len(nums), 2):
        p1, p2 = nums[i], nums[i + 1]
        c1 = (key_matrix[0][0] * p1 + key_matrix[0][1] * p2) % 26
        c2 = (key_matrix[1][0] * p1 + key_matrix[1][1] * p2) % 26
        cipher_nums.extend([c1, c2])
    return nums_to_text(cipher_nums)


def hill_decrypt(text, key_matrix):
    inv = matrix_inverse_2x2(key_matrix)
    if inv is None:
        raise ValueError("Key matrix is not invertible mod 26. Choose a different key.")
    nums = text_to_nums(text)
    plain_nums = []
    for i in range(0, len(nums), 2):
        c1, c2 = nums[i], nums[i + 1]
        p1 = (inv[0][0] * c1 + inv[0][1] * c2) % 26
        p2 = (inv[1][0] * c1 + inv[1][1] * c2) % 26
        plain_nums.extend([p1, p2])
    return nums_to_text(plain_nums)


# =========================================================================
# 6. Playfair Cipher
# =========================================================================
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