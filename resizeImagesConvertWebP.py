from PIL import Image
import glob, os

def toWebp():
  lst_imgs = [i for i in glob.glob("*.jpg")]

  for i in lst_imgs:
    fl, ext = os.path.splitext(i)
    img = Image.open(i).convert("RGB")
    basewidth = 1048
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(fl + ".webp", "WEBP", quality=50)

def toPng():
  lst_imgs = [i for i in glob.glob("*.webp")]

  for i in lst_imgs:
    fl, ext = os.path.splitext(i)
    img = Image.open(i).convert("RGB")
    basewidth = 1048
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(fl + ".png", "PNG")

toPng()