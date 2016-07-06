from app import app, SkinToSticker
from flask import request
import os, base64, json
from PIL import Image
from cStringIO import StringIO

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/stickerify', methods=['GET', 'POST'])
def receive_skin():
    if not request.json:
        abort(400)

    order_id = request.json['id']
    dt = request.json['created_at']
    dt.replace(':', '-')
    i = 0

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

        # Turn tge skin into a sticker and save it
        skinimg = Image.open(skinpath)
        sticker = SkinToSticker.stickerify(skinimg)
        stickerpath = os.path.join(app.config['STICKERS_FOLDER'], fname)
        sticker.save(stickerpath,"PNG")

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

        output = StringIO()
        skin.save(output, format='PNG')
        im_data = output.getvalue()
        imgstr = 'data:image/png;base64,' + base64.b64encode(im_data)

        order['img'] = imgstr
        responses.append(order)
    return json.dumps(responses)