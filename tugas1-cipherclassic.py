import math
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ===========Caesar
def caesar_encrypt(text, shift):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ===========Affine
def affine_encrypt(text, a, b):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        else:
            result += char
    return result

def affine_decrypt(text, a, b):
    result = ""
    if math.gcd(a, 26) != 1:
        return "Error: Nilai 'a' harus coprime dengan 26!"
    for i in range(26):
        if (a * i) % 26 == 1:
            a_inv = i
            break
    for char in text.upper():
        if char.isalpha():
            result += chr(((a_inv * ((ord(char) - 65) - b)) % 26) + 65)
        else:
            result += char
    return result

# ===========Vigenere
def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            result += chr(((ord(char) - 65 + shift) % 26) + 65)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            result += chr(((ord(char) - 65 - shift) % 26) + 65)
            key_index += 1
        else:
            result += char
    return result

# ===========Playfair
def generate_playfair_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace("J", "I")))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    for char in key + alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def playfair_prepare(text):
    text = text.upper().replace("J", "I")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i + 1 < len(text) else "X"
        if a == b:
            pairs.append((a, "X"))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    return pairs

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pairs = playfair_prepare("".join([c for c in text.upper() if c.isalpha()]))
    result = ""
    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            result += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    return result

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pairs = playfair_prepare(text)
    result = ""
    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            result += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    return result

# ===========Hill
def text_to_numbers(text):
    return [ord(c) - 65 for c in text.upper() if c.isalpha()]

def numbers_to_text(nums):
    return "".join(chr((n % 26) + 65) for n in nums)

def hill_encrypt(text, key_matrix):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += "X"
    result = ""
    for i in range(0, len(text), 2):
        pair = np.array([[ord(text[i]) - 65], [ord(text[i+1]) - 65]])
        encrypted = np.dot(key_matrix, pair) % 26
        result += chr(encrypted[0][0] + 65) + chr(encrypted[1][0] + 65)
    return result

def hill_decrypt(text, key_matrix):
    det = int(np.round(np.linalg.det(key_matrix))) % 26
    det_inv = None
    for i in range(26):
        if (det * i) % 26 == 1:
            det_inv = i
            break
    if det_inv is None:
        return "Error: Determinan tidak memiliki invers modulo 26!"

    adj = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
    inv_matrix = (det_inv * adj) % 26

    result = ""
    for i in range(0, len(text), 2):
        pair = np.array([[ord(text[i]) - 65], [ord(text[i+1]) - 65]])
        decrypted = np.dot(inv_matrix, pair) % 26
        result += chr(int(decrypted[0][0]) + 65) + chr(int(decrypted[1][0]) + 65)
    return result


# ===========Sistem
def export_to_file(metode, mode, teks_asli, hasil, shift=None, a=None, b=None):
    file_path = filedialog.asksaveasfilename(
        title="Simpan hasil sebagai...",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"=== {metode.upper()} ===\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Teks asli: {teks_asli}\n")
        if metode == "Caesar Cipher":
            f.write(f"Shift = {shift}\n")
        elif metode == "Affine Cipher":
            f.write(f"a = {a}\n")
            f.write(f"b = {b}\n")
        f.write("-" * 25 + "\n")
        f.write(f"Hasil: {hasil}\n")

    messagebox.showinfo("Berhasil", f"Hasil berhasil disimpan ke:\n{file_path}")

def jalankan_cipher():
    metode = combo_metode.get()
    mode = combo_mode.get()
    teks = entry_teks.get("1.0", "end-1c").strip()

    if not teks:
        messagebox.showerror("Error", "Teks tidak boleh kosong!")
        return

    hasil = ""
    try:
        if metode == "Caesar Cipher":
            shift = int(entry_shift.get())
            hasil = caesar_encrypt(teks, shift) if mode == "Encrypt" else caesar_decrypt(teks, shift)
        elif metode == "Affine Cipher":
            a = int(entry_a.get()); b = int(entry_b.get())
            hasil = affine_encrypt(teks, a, b) if mode == "Encrypt" else affine_decrypt(teks, a, b)
        elif metode == "Vigenere Cipher":
            key = entry_key_vig.get().strip()
            hasil = vigenere_encrypt(teks, key) if mode == "Encrypt" else vigenere_decrypt(teks, key)
        elif metode == "Playfair Cipher":
            key = entry_key_play.get().strip()
            hasil = playfair_encrypt(teks, key) if mode == "Encrypt" else playfair_decrypt(teks, key)
        elif metode == "Hill Cipher":
            try:
                key_text = entry_key_hill.get().strip().split(",")
                key_matrix = np.array([[int(key_text[0]), int(key_text[1])],
                                       [int(key_text[2]), int(key_text[3])]])
                hasil = hill_encrypt(teks, key_matrix) if mode == "Encrypt" else hill_decrypt(teks, key_matrix)
            except:
                messagebox.showerror("Error", "Key Hill harus dalam format: a,b,c,d (contoh: 3,3,2,5)")
                return
        else:
            messagebox.showerror("Error", "Pilih metode terlebih dahulu!")
            return
    except ValueError:
        messagebox.showerror("Error", "Nilai numerik tidak valid.")
        return

    text_hasil.config(state="normal")
    text_hasil.delete("1.0", "end")
    text_hasil.insert("1.0", hasil)
    text_hasil.config(state="disabled")

def simpan_hasil():
    metode = combo_metode.get()
    mode = combo_mode.get()
    teks_asli = entry_teks.get("1.0", "end-1c").strip()
    hasil = text_hasil.get("1.0", "end-1c").strip()
    if not hasil:
        messagebox.showwarning("Peringatan", "Belum ada hasil untuk disimpan.")
        return

    params = {}
    if metode == "Caesar Cipher":
        params["shift"] = entry_shift.get()
    elif metode == "Affine Cipher":
        params["a"] = entry_a.get(); params["b"] = entry_b.get()
    elif metode == "Vigenere Cipher":
        params["key"] = entry_key_vig.get()
    elif metode == "Playfair Cipher":
        params["key"] = entry_key_play.get()
    elif metode == "Hill Cipher":
        params["key"] = entry_key_hill.get()

    export_to_file(metode, mode, teks_asli, hasil, **params)

def update_fields(event=None):
    for frame in [frame_caesar, frame_affine, frame_vigenere, frame_playfair, frame_hill]:
        frame.grid_remove()
    metode = combo_metode.get()
    if metode == "Caesar Cipher":
        frame_caesar.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
    elif metode == "Affine Cipher":
        frame_affine.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
    elif metode == "Vigenere Cipher":
        frame_vigenere.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
    elif metode == "Playfair Cipher":
        frame_playfair.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
    elif metode == "Hill Cipher":
        frame_hill.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)

def tampilkan_info():
    metode = combo_metode.get()
    info_text = ""

    if metode == "Caesar Cipher":
        info_text = (
            "Caesar Cipher\n\n"
            "~ Enkripsi:\n"
            "Geser huruf sebanyak 'shift'.\n"
            "• Hanya huruf A-Z yang diproses.\n"
            "• Shift bisa positif (geser maju) atau negatif (geser mundur).\n"
            "Contoh: SHIFT=3, maka A→D, B→E, C→F.\n\n"
            "~ Dekripsi:\n"
            "Geser huruf ke arah sebaliknya sebanyak 'shift' yang sama.\n"
            "Contoh: SHIFT=3, maka D→A, E→B, F→C."
        )

    elif metode == "Affine Cipher":
        info_text = (
            "Affine Cipher\n\n"
            "~ Enkripsi:\n"
            "Gunakan rumus: E(x) = (a*x + b) mod 26.\n"
            "• 'a' harus coprime dengan 26 agar bisa didekripsi.\n"
            "• 'b' adalah nilai geser tambahan.\n"
            "Contoh: a=5, b=8, maka A→I, B→N, C→S.\n\n"
            "~ Dekripsi:\n"
            "Gunakan rumus: D(y) = a_inv * (y - b) mod 26.\n"
            "• a_inv adalah invers dari a (mod 26)."
        )

    elif metode == "Vigenere Cipher":
        info_text = (
            "Vigenere Cipher\n\n"
            "~ Enkripsi:\n"
            "Gunakan kunci alfabet tanpa spasi.\n"
            "• Setiap huruf kunci menentukan jumlah pergeseran.\n"
            "Contoh: KEY=LEMON, maka ATTACK → LXFOPV.\n\n"
            "~ Dekripsi:\n"
            "Gunakan rumus kebalikan:\n"
            "D(i) = (C(i) - K(i)) mod 26.\n"
            "• Huruf ciphertext dikembalikan sesuai nilai kunci."
        )

    elif metode == "Playfair Cipher":
        info_text = (
            "Playfair Cipher\n\n"
            "~ Enkripsi:\n"
            "Gunakan kunci teks untuk membuat tabel 5x5.\n"
            "• Huruf J digabung dengan I.\n"
            "• Enkripsi dilakukan per pasangan huruf.\n"
            "Contoh: KEY=MONARCHY, maka 'HELLO' → 'CFSUPM'.\n\n"
            "~ Dekripsi:\n"
            "Setiap pasangan huruf dibalik langkahnya:\n"
            "• Jika sejajar kolom, geser ke atas.\n"
            "• Jika sejajar baris, geser ke kiri.\n"
            "• Jika membentuk persegi, ambil huruf pada kolom berlawanan."
        )

    elif metode == "Hill Cipher":
        info_text = (
            "Hill Cipher\n\n"
            "~ Enkripsi:\n"
            "Gunakan matriks kunci (biasanya 2x2).\n"
            "• Huruf diubah ke angka 0–25.\n"
            "• Hasil = (Kunci × Vektor) mod 26.\n"
            "Contoh: K = [[3,3],[2,5]], maka 'HI' → 'TC'.\n\n"
            "~ Dekripsi:\n"
            "Gunakan invers dari matriks kunci (mod 26).\n"
            "• Hasil = (Kunci⁻¹ × Vektor Cipher) mod 26.\n"
            "• Matriks kunci harus memiliki determinan coprime dengan 26."
        )

    else:
        info_text = "Pilih metode cipher terlebih dahulu."

    messagebox.showinfo(f"Informasi {metode}", info_text)

# === GUI ===
root = tk.Tk()
root.title("Cipher Klasik - Caesar, Affine, Vigenere, Hill, Playfair")
root.geometry("550x600")
root.resizable(False, False)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Metode Cipher:").grid(row=0, column=0, sticky="w")
combo_metode = ttk.Combobox(frame, values=[
    "Caesar Cipher", "Affine Cipher", "Vigenere Cipher", "Playfair Cipher", "Hill Cipher"
], state="readonly")
combo_metode.grid(row=0, column=1, pady=5, sticky="w")
combo_metode.current(0)
combo_metode.bind("<<ComboboxSelected>>", update_fields)

ttk.Button(frame, text="?", width=3, command=tampilkan_info).grid(row=0, column=1, padx=(150,5), sticky="w") 

ttk.Label(frame, text="Mode:").grid(row=1, column=0, sticky="w")
combo_mode = ttk.Combobox(frame, values=["Encrypt", "Decrypt"], state="readonly")
combo_mode.grid(row=1, column=1, pady=5, sticky="w")
combo_mode.current(0)

ttk.Label(frame, text="Teks:").grid(row=2, column=0, sticky="nw")
entry_teks = tk.Text(frame, width=55, height=5)
entry_teks.grid(row=2, column=1, pady=5)

# === Frame Caesar ===
frame_caesar = ttk.LabelFrame(frame, text="Caesar Cipher", padding=10)
ttk.Label(frame_caesar, text="Shift:").grid(row=0, column=0, sticky="w")
entry_shift = ttk.Entry(frame_caesar, width=10)
entry_shift.grid(row=0, column=1, padx=5)

# === Frame Affine ===
frame_affine = ttk.LabelFrame(frame, text="Affine Cipher", padding=10)
ttk.Label(frame_affine, text="a:").grid(row=0, column=0, sticky="w")
entry_a = ttk.Entry(frame_affine, width=10)
entry_a.grid(row=0, column=1, padx=5)
ttk.Label(frame_affine, text="b:").grid(row=0, column=2, sticky="w")
entry_b = ttk.Entry(frame_affine, width=10)
entry_b.grid(row=0, column=3, padx=5)

# === Frame Vigenere ===
frame_vigenere = ttk.LabelFrame(frame, text="Vigenere Cipher", padding=10)
ttk.Label(frame_vigenere, text="Key:").grid(row=0, column=0, sticky="w")
entry_key_vig = ttk.Entry(frame_vigenere, width=20)
entry_key_vig.grid(row=0, column=1, padx=5)

# === Frame Playfair ===
frame_playfair = ttk.LabelFrame(frame, text="Playfair Cipher", padding=10)
ttk.Label(frame_playfair, text="Key:").grid(row=0, column=0, sticky="w")
entry_key_play = ttk.Entry(frame_playfair, width=20)
entry_key_play.grid(row=0, column=1, padx=5)

# === Frame Hill ===
frame_hill = ttk.LabelFrame(frame, text="Hill Cipher", padding=10)
ttk.Label(frame_hill, text="Key (4 angka, dipisah koma):").grid(row=0, column=0, sticky="w")
entry_key_hill = ttk.Entry(frame_hill, width=20)
entry_key_hill.insert(0, "3,3,2,5")
entry_key_hill.grid(row=0, column=1, padx=5)

update_fields()

ttk.Label(frame, text="Hasil:").grid(row=5, column=0, sticky="nw")
text_hasil = tk.Text(frame, width=55, height=6, state="disabled")
text_hasil.grid(row=5, column=1, pady=5)

btn_frame = ttk.Frame(frame)
btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
ttk.Button(btn_frame, text="Jalankan", command=jalankan_cipher).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Simpan Hasil", command=simpan_hasil).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Keluar", command=root.quit).grid(row=0, column=2, padx=5)

root.mainloop()