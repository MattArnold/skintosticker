import os
from app import app#, SkinToSticker
from flask import request

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
        fh = open(os.path.join(app.config['SKINS_FOLDER'], fname), 'wb')
        fh.write(skin.decode('base64'))
        fh.close()

    return ('Success', 201)