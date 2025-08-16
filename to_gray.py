# Módulo que gera uma imagem de 512x512px em grayscale a partir da ÚNICA (é necessário ter apenas uma) imagem na pasta \img_to_gray
# A imagem gerada é salva na pasta \imgs_gray


import os
from PIL import Image

# Caminhos das pastas
input_folder = ".\img_to_gray"
output_folder = ".\imgs_banco_gray"

# Garantir que a pasta de saída exista
os.makedirs(output_folder, exist_ok=True)

# Listar arquivos na pasta de entrada
files = os.listdir(input_folder)

# Garantir que há exatamente uma imagem
if len(files) != 1:
    raise ValueError("A pasta 'img_to_gray' deve conter exatamente uma imagem.")

# Pegar o nome do arquivo
filename = files[0]
input_path = os.path.join(input_folder, filename)

# Abrir a imagem
img = Image.open(input_path)

# Converter para tons de cinza e redimensionar
img_gray_resized = img.convert("L").resize((512, 512))

# Criar nome do arquivo de saída
name, ext = os.path.splitext(filename)
output_filename = f"{name}_512x512_gray{ext}"
output_path = os.path.join(output_folder, output_filename)

# Salvar imagem
img_gray_resized.save(output_path)

output_path
