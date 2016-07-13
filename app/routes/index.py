from app import app, SkinToSticker
from flask import request
import os, base64, json
from PIL import Image
from cStringIO import StringIO

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/paths', methods=['GET'])
def getpaths():
    return "%s %s" % (app.config['SKINS_FOLDER'], app.config['STICKERS_FOLDER'])

@app.route('/stickerify', methods=['GET', 'POST'])
def receive_skin():
    if not request.json:
        abort(400)

    if request.json['id']:
        order_id = request.json['id']
    else:
        order_id = 'no order id'

    if request.json['created_at']:
        dt = request.json['created_at']
        dt.replace(':', '-')
    else:
        dt = 'no datetime'

    i = 0
    if request.json['line_items']:
        line_items = request.json['line_items']
        for item in line_items:
            i += 1
            fname = '%s_%s_%d.png' % (order_id, dt, i)
            properties = item['properties']
            skin = properties[0]['uploadedskin']
            skinpath = os.path.join(app.config['SKINS_FOLDER'], fname)

            # Back up the original skin
            fh = open(skinpath, 'wb')
            writtenfile = fh.write(skin.decode('base64'))
            fh.close()

            # Turn the skin into a sticker and save it
            skinimg = Image.open(skinpath)
            sticker = SkinToSticker.stickerify(skinimg)
            stickerpath = os.path.join(app.config['STICKERS_FOLDER'], fname)
            sticker.save(stickerpath,"PNG")
    else:
        line_items = 'no line items'

    return ('Success', 201)

@app.route('/orders', methods=['GET'])
def list_orders():
    skinlist = os.listdir('app/static/skins')
    responses = []
    for fn in skinlist:
    	withextension = fn.split('.')
    	nonextension = withextension[0]
    	metadata = nonextension.split('_')
        order = {}
        order['fn'] = fn
        order['id'] = metadata[0]
        order['dt'] = metadata[1]
        order['item'] = metadata[2]

        skin = Image.open('app/static/skins/' + fn)
        skin_output = StringIO()
        skin.save(skin_output, format='PNG')
        skin_im_data = skin_output.getvalue()
        skin_img_str = 'data:image/png;base64,' + base64.b64encode(skin_im_data)
        order['skin'] = skin_img_str

        sticker = Image.open('app/static/stickers/' + fn)
        sticker_output = StringIO()
        sticker.save(sticker_output, format='PNG')
        sticker_im_data = sticker_output.getvalue()
        sticker_img_str = 'data:image/png;base64,' + base64.b64encode(sticker_im_data)
        order['sticker'] = sticker_img_str

        responses.append(order)
    return json.dumps(responses)