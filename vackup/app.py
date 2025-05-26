
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
from datetime import datetime

INTERVALO_HORAS = 12
LOG_PATH = "backup.log"

def log(mensagem):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{{data_hora}}] {{mensagem}}\n")

def selecionar_origem():
    pasta_origem = filedialog.askdirectory(title="Selecione a pasta de origem")
    if pasta_origem:
        entrada_origem.delete(0, tk.END)
        entrada_origem.insert(0, pasta_origem)

def selecionar_destino():
    arquivo_destino = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("Arquivos ZIP", "*.zip")],
        title="Salvar backup manual como"
    )
    if arquivo_destino:
        entrada_destino.delete(0, tk.END)
        entrada_destino.insert(0, arquivo_destino)

def criar_backup(origem, destino_base, usar_timestamp=False):
    try:
        if usar_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            destino_base += f"_{{timestamp}}"
        shutil.make_archive(destino_base, 'zip', origem)
        log(f"Backup realizado com sucesso: {{destino_base}}.zip")
        return True
    except Exception as e:
        log(f"Erro ao realizar backup: {{str(e)}}")
        return False

def fazer_backup():
    origem = entrada_origem.get()
    destino = entrada_destino.get()
    if not origem or not destino:
        messagebox.showwarning("Campos obrigatórios", "Preencha ambos os campos de origem e destino.")
        return
    sucesso = criar_backup(origem, os.path.splitext(destino)[0])
    if sucesso:
        messagebox.showinfo("Sucesso", f"Backup criado com sucesso em:\n{{destino}}")
    else:
        messagebox.showerror("Erro", "Ocorreu um erro ao criar o backup.")

def backup_automatico():
    while True:
        origem = entrada_origem.get()
        destino = entrada_destino.get()
        if origem and destino:
            destino_base = os.path.splitext(destino)[0]
            criar_backup(origem, destino_base, usar_timestamp=True)
        time.sleep(INTERVALO_HORAS * 3600)

def iniciar_backup_automatico():
    thread = threading.Thread(target=backup_automatico, daemon=True)
    thread.start()

janela = tk.Tk()
janela.title("Vackup - Backup ZIP Automático")
janela.geometry("500x250")

tk.Label(janela, text="Pasta de origem:").pack(pady=5)
entrada_origem = tk.Entry(janela, width=60)
entrada_origem.pack()
tk.Button(janela, text="Selecionar pasta", command=selecionar_origem).pack(pady=5)

tk.Label(janela, text="Salvar backup como:").pack(pady=5)
entrada_destino = tk.Entry(janela, width=60)
entrada_destino.pack()
tk.Button(janela, text="Selecionar destino", command=selecionar_destino).pack(pady=5)

tk.Button(janela, text="Fazer Backup Manual", command=fazer_backup, bg="green", fg="white").pack(pady=10)

iniciar_backup_automatico()
janela.mainloop()
