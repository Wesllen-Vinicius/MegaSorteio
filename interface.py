import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
from gerador import gerar_sorteio, JOGOS

class GeradorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Números Aleatórios")
        self.root.geometry("500x700")
        self.root.configure(bg="#f8f9fa")

        ttk.Label(self.root, text="Gerador de Conjunto de Jogos", font=("Helvetica", 16, 'bold')).pack(pady=10)

        ttk.Label(self.root, text="Escolha o tipo de jogo:").pack(pady=5)
        self.tipo_jogo = tk.StringVar(value="mega")
        self.opcoes_jogo = ttk.Combobox(self.root, textvariable=self.tipo_jogo, values=list(JOGOS.keys()), state="readonly")
        self.opcoes_jogo.pack(pady=5)

        ttk.Label(self.root, text="Quantos conjuntos gerar?").pack(pady=5)
        self.entry_conjuntos = ttk.Entry(self.root, font=("Helvetica", 12))
        self.entry_conjuntos.pack(pady=5, ipadx=10, ipady=5)

        self.botao_gerar = ttk.Button(self.root, text="Gerar Números", command=self.gerar_numeros)
        self.botao_gerar.pack(pady=10, ipadx=10, ipady=5)

        self.frame_resultado = ttk.Frame(self.root)
        self.frame_resultado.pack(pady=10, padx=10, fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame_resultado, bg="#f8f9fa")
        self.scrollbar = ttk.Scrollbar(self.frame_resultado, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)
        
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.botao_copiar = ttk.Button(self.root, text="Copiar Conjuntos", command=self.copiar_conjuntos, state=tk.DISABLED)
        self.botao_copiar.pack(pady=10, ipadx=10, ipady=5)
    
    def gerar_numeros(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            num_conjuntos = int(self.entry_conjuntos.get())
            if num_conjuntos <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido de conjuntos.")
            return

        tipo_jogo = self.tipo_jogo.get()
        conjuntos = []
        max_tentativas = 100
        
        for _ in range(num_conjuntos):
            tentativas = 0
            while tentativas < max_tentativas:
                try:
                    conjunto = gerar_sorteio(tipo_jogo)
                    conjuntos.append(conjunto)
                    break
                except Exception:
                    tentativas += 1
            
            if tentativas >= max_tentativas:
                messagebox.showerror("Erro", "Falha ao gerar alguns conjuntos. Verifique os critérios.")
                return

        for conjunto in conjuntos:
            ttk.Label(self.scroll_frame, text=", ".join(f"{num:02d}" for num in conjunto), font=("Helvetica", 10)).pack(anchor="w")

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.botao_copiar.config(state=tk.NORMAL)

    def copiar_conjuntos(self):
        text = "\n".join(widget.cget("text") for widget in self.scroll_frame.winfo_children())
        pyperclip.copy(text)
        messagebox.showinfo("Sucesso", "Conjuntos copiados para a área de transferência!")

def main():
    root = tk.Tk()
    app = GeradorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
