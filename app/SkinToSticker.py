from PIL import Image
def stickerify(skin):

  # Images are cropped in the order they appear on the original skin.
  # For reference, see the color-coded skin image: 1_8_texturemap_redux.png
  # Names ending with a "_" character are for the secondary layer.

  #top row
  headup          = skin.crop((8,0,16,8))
  headdown        = skin.crop((16,0,24,8))
  headup_         = skin.crop((40,0,48,8))
  headdown_       = skin.crop((48,0,56,8))
  #second row:
  headfrontsides  = skin.crop((0,8,24,16))
  headback        = skin.crop((24,8,32,16)).rotate(180)
  headfrontsides_ = skin.crop((32,8,56,16))
  headback_       = skin.crop((56,8,64,16)).rotate(180)
  #third row:
  rightlegup      = skin.crop((4,16,8,20))
  rightlegdown    = skin.crop((8,16,12,20))
  bodyup          = skin.crop((20,16,28,20))
  bodydown        = skin.crop((28,16,34,20))
  rightarmup      = skin.crop((44,16,48,20))
  rightarmdown    = skin.crop((48,16,52,20))
  #fourth row:
  rightlegout     = skin.crop((0,20,4,32))
  rightlegfront   = skin.crop((4,20,8,32))
  rightlegin      = skin.crop((8,20,12,32))
  rightlegback    = skin.crop((12,20,16,32)).rotate(180)
  bodyfrontsidesback = skin.crop((16,20,40,32))
  rightarmfrontsides = skin.crop((40,20,52,32))
  rightarmback    = skin.crop((52,20,56,32))
  #fifth row:
  rightlegup_     = skin.crop((4,32,8,36))
  rightlegdown_   = skin.crop((8,32,12,36))
  bodyup_         = skin.crop((20,32,28,36))
  bodydown_       = skin.crop((28,32,36,36))
  rightarmup_     = skin.crop((44,32,48,36))
  rightarmdown_   = skin.crop((48,32,52,36))
  #sixth row:
  rightlegout_    = skin.crop((0,36,4,48))
  rightlegfront_  = skin.crop((4,36,8,48))
  rightlegin_     = skin.crop((8,36,12,48))
  rightlegback_   = skin.crop((12,36,16,48)).rotate(180)
  bodyfrontsidesback_ = skin.crop((16,36,40,48))
  rightarmfrontsides_ = skin.crop((40,36,52,48))
  rightarmback_   = skin.crop((52,36,56,48))
  #seventh row:
  leftlegup_      = skin.crop((20,48,24,52))
  leftlegdown_    = skin.crop((24,48,28,52))
  leftlegup       = skin.crop((20,48,24,52))
  leftlegdown     = skin.crop((24,48,28,52))
  leftarmup       = skin.crop((36,48,40,52))
  leftarmdown     = skin.crop((40,48,44,52))
  leftarmup_      = skin.crop((52,48,56,52))
  leftarmdown_    = skin.crop((56,48,60,52))
  #eighth row:
  leftlegout_     = skin.crop((0,52,4,64))
  leftlegfront_   = skin.crop((4,52,8,64))
  leftlegin_      = skin.crop((8,52,12,64))
  leftlegback_    = skin.crop((12,52,16,64)).rotate(180)
  leftlegout      = skin.crop((16,52,20,64))
  leftlegfront    = skin.crop((20,52,24,64))
  leftlegin       = skin.crop((24,52,28,64))
  leftlegback     = skin.crop((28,52,32,64)).rotate(180)
  leftarmfrontsides = skin.crop((32,52,44,64))
  leftarmback     = skin.crop((44,52,48,64))
  leftarmfrontsides_ = skin.crop((48,52,60,64))
  leftarmback_     = skin.crop((60,52,64,64))


  # Overlay the secondary layer on each image

  headup.paste(headup_, (0, 0), headup_)
  headdown.paste(headdown_, (0, 0), headdown_)
  headfrontsides.paste(headfrontsides_, (0, 0), headfrontsides_)
  headback.paste(headback_, (0, 0), headback_)
  rightlegup.paste(rightlegup_, (0, 0), rightlegup_)
  rightlegdown.paste(rightlegdown_, (0, 0), rightlegdown_)
  bodyup.paste(bodyup_, (0, 0), bodyup_)
  bodydown.paste(bodydown_, (0, 0), bodydown_)
  rightarmup.paste(rightarmup_, (0, 0), rightarmup_)
  rightarmdown.paste(rightarmdown_, (0, 0), rightarmdown_)
  rightlegout.paste(rightlegout_, (0, 0), rightlegout_)
  rightlegfront.paste(rightlegfront_, (0, 0), rightlegfront_)
  rightlegin.paste(rightlegin_, (0, 0), rightlegin_)
  rightlegback.paste(rightlegback_, (0, 0), rightlegback_)
  bodyfrontsidesback.paste(bodyfrontsidesback_, (0, 0), bodyfrontsidesback_)
  rightarmfrontsides.paste(rightarmfrontsides_, (0, 0), rightarmfrontsides_)
  rightarmback.paste(rightarmback_, (0, 0), rightarmback_)
  leftlegup.paste(leftlegup_, (0, 0), leftlegup_)
  leftlegdown.paste(leftlegdown_, (0, 0), leftlegdown_)
  leftarmup.paste(leftarmup_, (0, 0), leftarmup_)
  leftarmdown.paste(leftarmdown_, (0, 0), leftarmdown_)
  leftlegout.paste(leftlegout_, (0, 0), leftlegout_)
  leftlegin.paste(leftlegin_, (0, 0), leftlegin_)
  leftlegback.paste(leftlegback_, (0, 0), leftlegback_)
  leftlegfront.paste(leftlegfront_, (0, 0), leftlegfront_)
  leftarmfrontsides.paste(leftarmfrontsides_, (0, 0), leftarmfrontsides_)
  leftarmback.paste(leftarmback_, (0, 0), leftarmback_)


  # Create a blank image

  sticker = Image.new("RGBA", (68,68), (255,0,0,0))

  # Arrange the cropped images on the sticker image

  sticker.paste(headup,         (10,10))
  sticker.paste(headdown,       (10,26))
  sticker.paste(headfrontsides, (2,18))
  sticker.paste(headback,       (10,2))

  sticker.paste(rightlegout,    (30,2))
  sticker.paste(rightlegdown,   (30,14))
  sticker.paste(rightlegin,     (30,18))
  sticker.paste(rightlegup,     (38,14))
  sticker.paste(rightlegback,   (38,2))
  sticker.paste(rightlegfront,  (38,17))

  sticker.paste(leftlegout,    (46,2))
  sticker.paste(leftlegdown,   (46,14))
  sticker.paste(leftlegin,     (46,18))
  sticker.paste(leftlegup,     (54,14))
  sticker.paste(leftlegback,   (54,2))
  sticker.paste(leftlegfront,  (54,17))

  sticker.paste(rightarmfrontsides, (22,46))
  sticker.paste(rightarmback,  (34,46))
  sticker.paste(rightarmup,    (26,42))
  sticker.paste(rightarmdown,  (26,58))

  sticker.paste(leftarmfrontsides, (2,46))
  sticker.paste(leftarmback,  (14,46))
  sticker.paste(leftarmup,    (2,42))
  sticker.paste(leftarmdown,  (2,58))

  sticker.paste(bodyup,        (46,42))
  sticker.paste(bodydown,      (46,58))
  sticker.paste(bodyfrontsidesback, (42,46))


  # If the skin is the 32px high format, mirror the right limbs on the left limbs
  width, height = skin.size

  if height < 64:
    leftlegout = rightlegout.transpose(Image.FLIP_LEFT_RIGHT)
    leftlegdown = rightlegdown.transpose(Image.FLIP_LEFT_RIGHT)
    leftlegin = rightlegin.transpose(Image.FLIP_LEFT_RIGHT)
    leftlegup = rightlegup.transpose(Image.FLIP_LEFT_RIGHT)
    leftlegback = rightlegback.transpose(Image.FLIP_LEFT_RIGHT)
    leftlegfront = rightlegfront.transpose(Image.FLIP_LEFT_RIGHT)
    leftarmfrontsides = rightarmfrontsides.transpose(Image.FLIP_LEFT_RIGHT)
    leftarmback = rightarmback.transpose(Image.FLIP_LEFT_RIGHT)
    leftarmup = rightarmup.transpose(Image.FLIP_LEFT_RIGHT)
    leftarmdown = rightarmdown.transpose(Image.FLIP_LEFT_RIGHT)

    sticker.paste(leftlegout,    (46,2))
    sticker.paste(leftlegdown,   (46,14))
    sticker.paste(leftlegin,     (46,18))
    sticker.paste(leftlegup,     (54,14))
    sticker.paste(leftlegback,   (54,2))
    sticker.paste(leftlegfront,  (54,17))

    sticker.paste(leftarmfrontsides, (2,46))
    sticker.paste(leftarmback,  (14,46))
    sticker.paste(leftarmup,    (2,42))
    sticker.paste(leftarmdown,  (2,58))

  sticker = sticker.resize((792,792))

  return sticker