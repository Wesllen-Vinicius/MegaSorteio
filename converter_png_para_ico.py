# converter_png_para_ico.py
from PIL import Image

# Função para converter PNG para ICO
def converter_png_para_ico(png_file, ico_file):
    imagem_png = Image.open(png_file)  # Carregar o PNG
    imagem_png.save(ico_file, format="ICO")  # Salvar como ICO

# Converter icone.png para icone.ico
if __name__ == "__main__":
    converter_png_para_ico("icone.png", "icone.ico")
    print("Conversão concluída: icone.png para icone.ico")
