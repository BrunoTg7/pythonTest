from rembg import remove
from PIL import Image, ImageEnhance

# Abra a imagem de entrada
input_image = Image.open("imgfundo.jpg")

# Reduzir o tamanho da imagem para melhorar a precisão (opcional)
small_image = input_image.resize((input_image.width // 2, input_image.height // 2))

# Aumente o contraste da imagem para melhorar a remoção do fundo
enhancer = ImageEnhance.Contrast(small_image)
enhanced_image = enhancer.enhance(1.5)

# Remova o fundo usando o modelo 'u2net'
output_image = remove(enhanced_image)

# Redimensionar a imagem de volta ao tamanho original (opcional)
output_image = output_image.resize((input_image.width, input_image.height))

# Salve a imagem resultante no formato PNG
output_image.save("img1.png")
