import os
from PIL import Image

def concat(up: Image.Image, down: Image.Image):
    upw, uph = up.size
    dnw, dnh = down.size

    if upw != dnw:
        dnh *= upw / dnw
        dnw = upw
        down.resize((dnw, dnh), Image.BILINEAR)
    
    result = Image.new(down.mode, (upw, uph + dnh))
    result.paste(up, box=(0, 0))
    result.paste(down, box=(0, uph))
    return result

def crop(img: Image.Image, down=False):
    p = 80
    w, h = img.size
    box = (0, p, w, h) if down else (0, 0, w, p)
    return img.crop(box)

if __name__ == '__main__':
    os.chdir('..')
    up_names =[up for up in os.listdir('up') if up.endswith('.jpg')]

    ups = {up_name :crop(Image.open('up/' + up_name)) for up_name in up_names}
    down = Image.open('down/' + [down for down in os.listdir('down') if down.endswith('.jpg')][0])
    down = crop(down, down=True)

    for name, up in ups.items():
        result = concat(up, down)
        result.save('result/' + name)
    