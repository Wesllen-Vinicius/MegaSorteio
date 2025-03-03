import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import pyperclip  # Para copiar para a área de transferência
from gerador import carregar_numeros_excluidos, gerar_numeros

class GeradorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Números Aleatórios")
        self.root.geometry("500x500")  # Tamanho fixo
        self.root.config(bg="#f0f4f8")  # Cor de fundo suave
        
        # # Adicionando o ícone à aplicação
        # self.root.iconbitmap("icone.ico") 

        # Centralizar a janela
        self.center_window()

        # Definindo título
        self.label_titulo = tk.Label(self.root, text="Gerador de Números", font=("Helvetica", 16, 'bold'), bg="#f0f4f8", fg="#4f6d7a")
        self.label_titulo.pack(pady=20)

        # Botão para carregar o arquivo
        self.botao_carregar = tk.Button(self.root, text="Carregar Arquivo", command=self.carregar_arquivo, font=("Helvetica", 12), bg="#4f6d7a", fg="white", relief="solid", bd=1)
        self.botao_carregar.pack(pady=10, ipadx=10, ipady=5)

        # Área para mostrar o caminho do arquivo carregado
        self.label_arquivo = tk.Label(self.root, text="Nenhum arquivo carregado.", font=("Helvetica", 10), bg="#f0f4f8", fg="#4f6d7a")
        self.label_arquivo.pack(pady=5)

        # Campo de entrada para número de conjuntos
        self.label_num_conjuntos = tk.Label(self.root, text="Quantos conjuntos gerar?", font=("Helvetica", 10), bg="#f0f4f8", fg="#4f6d7a")
        self.label_num_conjuntos.pack(pady=5)
        
        self.entry_conjuntos = tk.Entry(self.root, font=("Helvetica", 12), bg="white", fg="#4f6d7a", relief="solid", bd=1)
        self.entry_conjuntos.pack(pady=5, ipadx=10, ipady=5)

        # Botão para gerar os números
        self.botao_gerar = tk.Button(self.root, text="Gerar Números", command=self.gerar_numeros, font=("Helvetica", 12), bg="#4f6d7a", fg="white", relief="solid", bd=1, state=tk.DISABLED)
        self.botao_gerar.pack(pady=10, ipadx=10, ipady=5)

        # Botão de copiar (inicialmente desabilitado)
        self.botao_copiar = tk.Button(self.root, text="Copiar Conjuntos", command=self.copiar_conjuntos, font=("Helvetica", 12), bg="#4f6d7a", fg="white", relief="solid", bd=1, state=tk.DISABLED)
        self.botao_copiar.pack(pady=10, ipadx=10, ipady=5)

        # Barra de progresso para mostrar carregamento
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="indeterminate")
        self.progress_bar.place_forget()  # Esconde a barra inicialmente

        # Scrollable frame for the generated numbers
        self.frame_scrollable = tk.Frame(self.root, bg="#f0f4f8")
        self.frame_scrollable.pack(pady=20, padx=20, fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame_scrollable, bg="#f0f4f8")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_scrollable, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.frame_conjuntos = tk.Frame(self.canvas, bg="#f0f4f8")
        self.canvas.create_window((0, 0), window=self.frame_conjuntos, anchor="nw")

        self.frame_conjuntos.bind("<Configure>", self.on_frame_configure)  # Redimensiona a tela quando necessário

        # Variável para armazenar os números excluídos
        self.numeros_excluidos = []

    def center_window(self):
        """Centraliza a janela na tela."""
        width = 500
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)

        self.root.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def carregar_arquivo(self):
        """Abrir o diálogo para carregar o arquivo de números excluídos."""
        arquivo = filedialog.askopenfilename(title="Escolha um arquivo", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if arquivo:
            try:
                # Carregar os números excluídos
                self.numeros_excluidos = carregar_numeros_excluidos(arquivo)
                self.label_arquivo.config(text=f"Arquivo carregado: {arquivo.split('/')[-1]}")
                self.botao_gerar.config(state=tk.NORMAL)  # Habilitar o botão de gerar números
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao ler o arquivo: {str(e)}")
                self.label_arquivo.config(text="Erro ao carregar arquivo.")

    def gerar_numeros(self):
        """Gerar os números aleatórios em uma thread separada e atualizar a interface."""
        if not self.numeros_excluidos:
            messagebox.showwarning("Aviso", "Nenhum arquivo carregado.")
            return

        try:
            # Recuperar a quantidade de conjuntos a serem gerados
            num_conjuntos = int(self.entry_conjuntos.get())
            if num_conjuntos <= 0:
                raise ValueError("A quantidade de conjuntos deve ser maior que 0.")
        except ValueError as ve:
            messagebox.showerror("Erro", f"Erro na entrada: {str(ve)}")
            return
        
        # Esconder a área de resultado enquanto gera os números
        self.label_resultado = tk.Label(self.frame_conjuntos, text="Gerando números...", font=("Helvetica", 12), bg="#f0f4f8", fg="#4f6d7a")
        self.label_resultado.grid(row=0, column=0, pady=20)

        # Exibir a barra de progresso
        self.progress_bar.place(x=50, y=160)
        self.progress_bar.start()

        # Criar uma nova thread para gerar os números
        thread = threading.Thread(target=self._gerar_numeros_em_background, args=(num_conjuntos,))
        thread.start()

    def _gerar_numeros_em_background(self, num_conjuntos):
        """Função para rodar em segundo plano, gerando os números e atualizando a interface."""
        try:
            # Gerar os conjuntos de números
            conjuntos_gerados = [gerar_numeros(self.numeros_excluidos) for _ in range(num_conjuntos)]
            
            # Atualizar a interface com os números gerados
            self.root.after(0, self._atualizar_resultado, conjuntos_gerados)
        except ValueError as e:
            # Em caso de erro, mostrar a mensagem ao usuário
            self.root.after(0, self._mostrar_erro, str(e))
        finally:
            # Parar a barra de progresso
            self.root.after(0, self.progress_bar.stop)
            self.root.after(0, self.progress_bar.place_forget)  # Esconder a barra de progresso

    def _atualizar_resultado(self, conjuntos):
        """Atualiza o rótulo com os números gerados."""
        for widget in self.frame_conjuntos.winfo_children():
            widget.destroy()  # Limpar a área de resultados antigos

        for i, conjunto in enumerate(conjuntos):
            label = tk.Label(self.frame_conjuntos, text=f"Conjunto {i+1}: {', '.join(map(str, conjunto))}", font=("Helvetica", 10), bg="#f0f4f8", fg="#4f6d7a")
            label.grid(row=i, column=0, pady=5, sticky="w")
        
        # Habilitar o botão de copiar
        self.botao_copiar.config(state=tk.NORMAL)

        # Atualizar a barra de rolagem
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _mostrar_erro(self, erro):
        """Exibe uma mensagem de erro ao usuário."""
        messagebox.showerror("Erro", erro)

    def copiar_conjuntos(self):
        """Copiar os conjuntos gerados para a área de transferência."""
        conjuntos = []
        for widget in self.frame_conjuntos.winfo_children():
            if isinstance(widget, tk.Label):
                conjuntos.append(widget.cget("text").split(":")[1].strip())

        # Copiar os conjuntos formatados como números separados por vírgulas
        pyperclip.copy("\n".join(conjuntos))
        messagebox.showinfo("Sucesso", "Conjuntos copiados para a área de transferência!")

    def on_frame_configure(self, event):
        """Atualiza a região de rolagem quando o conteúdo do frame é alterado."""
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

# Função para rodar o aplicativo
def main():
    root = tk.Tk()
    app = GeradorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
