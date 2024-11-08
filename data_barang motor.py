from itertools import tee
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json

FILENAME = 'data_motor.json'

data_array = []

def baca_dari_file():
    try:
        with open(FILENAME, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):  
        return []

def tampilkan_data(tree):
    for row in tree.get_children():
        tree.delete(row)
    
    data_array = baca_dari_file()
    for data in data_array:
        tree.insert("", tk.END, values=data)

def simpan_ke_file(data):
    with open(FILENAME, 'w') as file:
        json.dump(data, file)

def tampilan_tambah_motor():
    clear_widgets()
    nama_motor = simpledialog.askstring("Tambah Data Motor", "Masukkan nama motor:")
    merek_motor = simpledialog.askstring("Tambah Data Motor", "Masukkan merek motor:")
    jenis_motor = simpledialog.askstring("Tambah Data Motor", "Masukkan jenis motor:")
    warna_motor = simpledialog.askstring("Tambah Data Motor", "Masukkan warna motor:")
    noplat_motor = simpledialog.askstring("Tambah Data Motor", "Masukkan noplat motor:")
    
    data_array.append([nama_motor, merek_motor, jenis_motor, warna_motor, noplat_motor])
    simpan_ke_file(data_array)

def hapus_motor():
    nama_motor = simpledialog.askstring("Hapus Data Motor", "Masukkan nama motor yang ingin dihapus:")
    for motor in data_array:
        if motor[0] == nama_motor:
            data_array.remove(motor)
            simpan_ke_file(data_array)
            messagebox.showinfo("Info", f"Motor '{nama_motor}' berhasil dihapus!")
            return
    messagebox.showwarning("Warning", f"Motor '{nama_motor}' tidak ditemukan.")

def tampilan_data():
    clear_widgets()
    root = tk.Toplevel()
    root.title("Tampilan Data Motor")
    columns = ('Nama Motor', 'Merek Motor', 'Jenis Motor', 'Warna Motor', 'NoPlat Motor')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=0, column=0, padx=10, pady=10)

    btn_tampilkan = tk.Button(root, text="Tampilkan Data", command=lambda: tampilkan_data(tree))
    btn_tampilkan.grid(row=1, column=0, pady=10)
    
    tk.Button(root, text="Kembali ke Menu Utama", command=tampilan_menu_utama).grid(row=2, column=0)

def sort_data():
    clear_widgets()
    global data_array
    data_array = sorted(data_array, key=lambda x: x[0])  # Sort by first element (Nama Motor)
    simpan_ke_file(data_array)
    messagebox.showinfo("Info", "Data berhasil diurutkan!")

def search_data():
    clear_widgets()
    query = simpledialog.askstring("Search Motor", "Masukkan nama motor yang dicari:")
    results = [motor for motor in data_array if query.lower() in motor[0].lower()]
    
    if results:
        tampilkan_hasil_pencarian(results)
    else:
        messagebox.showinfo("Info", "Motor tidak ditemukan.")
        
class rental_Node:
    def __init__(self, rental_id, customer, take_date):
        self.rental_id = rental_id
        self.customer = customer
        self.take_date = take_date
        self.next = None

class rental_LinkedList:
    def __init__(self):
        self.head = None

    def push(self, rental_id, customer, take_date):
        new_node = rental_Node(rental_id, customer, take_date)

        new_node.next = self.head
        self.head = new_node

    def display(self):
        current_node = self.head

        while current_node:
            print(f'ID: {current_node.rental_id}, Customer: {current_node.customer} , take_date: {current_node.take_date}')
            current_node = current_node.next
    
    def delete(self,key):
        current_node = self.head
        prev_node = None

        if current_node is not None and current_node.rental_id == key:
            self.head = current_node.next
            current_node = None
            return 

        while current_node is not None and current_node.rental_id != key:
            prev_node = current_node
            current_node = current_node.next 

        if current_node is None:
            print(f"Node dengan data '{key}' tidak ditemukan.")
            return

        prev_node.next = current_node.next
        current_node = None    

sll = rental_LinkedList()
sll.push(301, "Agus", "2024-10-21")
sll.push(302, "Ayu", "2024-10-24")
sll.push(303, "Pupsita", "2024-04-28")
sll.push(304, "Jaya", "2024-04-20")

print("Data Reparasi:")
sll.display()
        
print("Menghapus Data: 302")
sll.delete(302)

print("Hasil data Setelah Hapus:")
sll.display()
        

def tampilkan_hasil_pencarian(results):
    root = tk.Toplevel()
    root.title("Hasil Pencarian")
    columns = ('Nama Motor', 'Merek Motor', 'Jenis Motor', 'Warna Motor', 'NoPlat Motor')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=0, column=0, padx=10, pady=10)

    for data in results:
        tree.insert("", tk.END, values=data)

    tk.Button(root, text="Kembali ke Menu Utama", command=tampilan_menu_utama).grid(row=1, column=0)

def tampilkan_menu(pilihan):
    clear_widgets()
    if pilihan == "Tambah Data Motor":
        tampilan_tambah_motor()
    elif pilihan == "Data Motor":
        tampilan_data()
    elif pilihan == "Hapus Data Motor":
        hapus_motor()
    elif pilihan == "Sort Data Motor":
        sort_data()
    elif pilihan == "Search Data Motor":
        search_data()
    else:
        messagebox.showwarning("Warning", "Pilihan tidak valid!")  

def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

def tampilan_menu_utama():
    clear_widgets()
    label_judul = tk.Label(root, text="Selamat Datang di Rental Motor", font=("Arial", 16))
    label_judul.pack(pady=20)

    opsi = ["Tambah Data Motor", "Data Motor", "Hapus Data Motor", "Sort Data Motor", "Search Data Motor"]
    combo_box = ttk.Combobox(root, values=opsi)
    combo_box.pack(pady=10)

    btn_pilih = tk.Button(root, text="Pilih", command=lambda: tampilkan_menu(combo_box.get()))
    btn_pilih.pack(pady=10)
    
root = tk.Tk()
root.title("Menu Rental Motor")

data_array = baca_dari_file()
tampilan_menu_utama()
root.mainloop()