import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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
            a = int(entry_a.get())
            b = int(entry_b.get())
            hasil = affine_encrypt(teks, a, b) if mode == "Encrypt" else affine_decrypt(teks, a, b)
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

    if metode == "Caesar Cipher":
        shift = entry_shift.get()
        export_to_file(metode, mode, teks_asli, hasil, shift=shift)
    elif metode == "Affine Cipher":
        a = entry_a.get()
        b = entry_b.get()
        export_to_file(metode, mode, teks_asli, hasil, a=a, b=b)

def update_fields(event=None):
    metode = combo_metode.get()
    if metode == "Caesar Cipher":
        frame_affine.grid_remove()
        frame_caesar.grid()
    elif metode == "Affine Cipher":
        frame_caesar.grid_remove()
        frame_affine.grid()

# === GUI utama ===
root = tk.Tk()
root.title("Cipher GUI - Mister Sopian")
root.geometry("520x540")
root.resizable(False, False)

# === input frame ===
frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Metode Cipher:").grid(row=0, column=0, sticky="w")
combo_metode = ttk.Combobox(frame, values=["Caesar Cipher", "Affine Cipher"], state="readonly")
combo_metode.grid(row=0, column=1, pady=5)
combo_metode.current(0)
combo_metode.bind("<<ComboboxSelected>>", update_fields)

ttk.Label(frame, text="Mode:").grid(row=1, column=0, sticky="w")
combo_mode = ttk.Combobox(frame, values=["Encrypt", "Decrypt"], state="readonly")
combo_mode.grid(row=1, column=1, pady=5)
combo_mode.current(0)

ttk.Label(frame, text="Teks:").grid(row=2, column=0, sticky="nw")
entry_teks = tk.Text(frame, width=50, height=5)
entry_teks.grid(row=2, column=1, pady=5)

# === untuk caesar ui ===
frame_caesar = ttk.LabelFrame(frame, text="Caesar Cipher", padding=10)
frame_caesar.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
ttk.Label(frame_caesar, text="Shift:").grid(row=0, column=0, sticky="w")
entry_shift = ttk.Entry(frame_caesar, width=10)
entry_shift.grid(row=0, column=1, padx=5)

# === untuk affine ui ===
frame_affine = ttk.LabelFrame(frame, text="Affine Cipher", padding=10)
frame_affine.grid(row=4, column=0, columnspan=2, sticky="we", pady=5)
ttk.Label(frame_affine, text="a:").grid(row=0, column=0, sticky="w")
entry_a = ttk.Entry(frame_affine, width=10)
entry_a.grid(row=0, column=1, padx=5)
ttk.Label(frame_affine, text="b:").grid(row=0, column=2, sticky="w")
entry_b = ttk.Entry(frame_affine, width=10)
entry_b.grid(row=0, column=3, padx=5)

# Default
update_fields()

# === ui hasil ===
ttk.Label(frame, text="Hasil:").grid(row=5, column=0, sticky="nw")
text_hasil = tk.Text(frame, width=50, height=6, state="disabled")
text_hasil.grid(row=5, column=1, pady=5)

# === ui tombol ===
btn_frame = ttk.Frame(frame)
btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

ttk.Button(btn_frame, text="Jalankan", command=jalankan_cipher).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Simpan Hasil", command=simpan_hasil).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Keluar", command=root.quit).grid(row=0, column=2, padx=5)

root.mainloop()