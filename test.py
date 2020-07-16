from PIL import Image, ImageOps

src = 'C:\\Users\\kuchida\\Desktop\\hokuren\\20200622\\ミラー型撮影装置\\_DSC1444.JPG'
img = Image.open(src)
img = img.resize((int(img.width / 4), int(img.height / 4)))
img = img.transpose(Image.ROTATE_180)
img = ImageOps.mirror(img)
img.save(src + '_2.jpg')