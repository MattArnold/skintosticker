from app import app, SkinToSticker
from flask import request, json, abort
import os, base64, urllib, shutil
from PIL import Image
from cStringIO import StringIO
import shippo
import requests

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/paths', methods=['GET', 'POST'])
def getpaths():
    return "%s %s" % (app.config['SKINS_FOLDER'], app.config['STICKERS_FOLDER'])

@app.route('/stickerify', methods=['GET', 'POST'])
def receive_skin():
    if not request.json:
        abort(400)

    order_id = 'no order id'
    dt = 'no datetime'
    character = app.config['FAILEDIMG']
    skin = app.config['FAILEDIMG']
    character_name = 'no character name'

    if request.json['id']:
        order_id = request.json['id']

    if request.json['created_at']:
        dt = request.json['created_at']
        dt.replace(':', '-')

    i = 0
    if request.json['line_items']:
        line_items = request.json['line_items']
        for item in line_items:
            i += 1
            properties = item['properties']
            for property in properties:
                property_name = property['name']
                if property['name'] == '_character':
                    character = property['value'][22:]
                elif property['name'] == '_skin':
                    skin = property['value'][22:]
                elif property['name'] == '_character_name':
                    character_name = property['value']

            # character_name = properties[2]['value'] # properties[2] will be the character's name
            fname = '%s_%s_%d_%s.png' % (order_id, dt, i, character_name)
            svgname = '%s_%s_%d_%s.svg' % (order_id, dt, i, character_name)

            # Save the preview image
            # character = properties[1]['value'][22:] # properties[1] will be the preview image
            characterpath = os.path.join(app.config['CHARACTERS_FOLDER'], fname)
            characterfh = open(characterpath, 'wb')
            try:
                characterfh.write(properties['_character'][22:].decode('base64'))
            except:
                characterfh.write(app.config['FAILEDIMG'][22:].decode('base64'))
            characterfh.close()

            # Save the original skin
            # skin = properties[0]['value'][22:] # properties[0] will be the skin
            skinpath = os.path.join(app.config['SKINS_FOLDER'], fname)
            skinfh = open(skinpath, 'wb')
            try:
                skinfh.write(properties['_skin'][22:].decode('base64'))
            except:
                skinfh.write(app.config['FAILEDIMG'][22:].decode('base64'))
            skinfh.close()

            # Turn the skin into a sticker and save it
            sticker_path = os.path.join(app.config['STICKERS_FOLDER'], fname)
            skinimg = Image.open(skinpath)
            sticker = SkinToSticker.stickerify(skinimg)
            sticker.save(sticker_path,"PNG")

    else:
        line_items = 'no line items'

    if request.json['shipping_address']:
        shipping_address = request.json['shipping_address']
        shippo.api_key = "bf261a7488fe66cc07bc5b02340d1e0e189b4932"

        address_from = {
            "object_purpose": "PURCHASE",
            "name": "Thad Johnson",
            "company": "Player Craft Toys",
            "street1": "1533 Surrey Ln",
            "city": "Rochester Hills",
            "state": "MI",
            "zip": "48306",
            "country": "US",
            "phone": "+1 810 287 3443",
            "email": "thad@criticalmovesusa.com"
        }

        address_to = {
            "object_purpose": "PURCHASE",
            "name": shipping_address['name'],
            "company": shipping_address['company'],
            "street1": shipping_address['address1'],
            "street2": shipping_address['address2'],
            "city": shipping_address['city'],
            "state": shipping_address['province'],
            "zip": shipping_address['zip'],
            "country": shipping_address['country_code'],
            "phone": shipping_address['phone'],
            "email": "example@example.com",
            "metadata": ""
        }

        parcel = {
            "length": "5",
            "width": "3",
            "height": "2",
            "distance_unit": "in",
            "weight": "2",
            "mass_unit": "oz"
        }

        shipment = {
            "object_purpose": "PURCHASE",
            "address_from": address_from,
            "address_to": address_to,
            "parcel": parcel
        }

        transaction = shippo.Transaction.create(
            shipment = shipment,
            carrier_account = "143a2a16ee3a4a1a822d8d326df667f3",
            servicelevel_token = "usps_first",
            label_file_type = "PNG"
        )

        label_url = transaction.label_url
        tracking_number = transaction.tracking_number
        tracking_url_provider = transaction.tracking_url_provider

        label_file = StringIO(urllib.urlopen(label_url).read())
        label = Image.open(label_file)
        label_path = os.path.join(app.config['LABELS_FOLDER'], fname)
        label.save(label_path,"PNG")

    return ('Success', 201)

@app.route('/orders', methods=['GET'])
def list_orders():
    skinlist = os.listdir(app.config['SKINS_FOLDER'])
    responses = []

    for fn in skinlist:
        order = extract_metadata(fn)

        if os.path.isfile(app.config['CHARACTERS_FOLDER'] + fn):
            character = Image.open(app.config['CHARACTERS_FOLDER'] + fn)
            character_output = StringIO()
            character.save(character_output, format='PNG')
            character_im_data = character_output.getvalue()
            character_img_str = 'data:image/png;base64,' + base64.b64encode(character_im_data)
        else:
            character_img_str = app.config['FAILEDIMG']

        order['character'] = character_img_str

        skin = Image.open(app.config['SKINS_FOLDER'] + fn)
        skin_output = StringIO()
        skin.save(skin_output, format='PNG')
        skin_im_data = skin_output.getvalue()
        skin_img_str = 'data:image/png;base64,' + base64.b64encode(skin_im_data)
        order['skin'] = skin_img_str

        if os.path.isfile(app.config['STICKERS_FOLDER'] + fn):
            sticker = Image.open(app.config['STICKERS_FOLDER'] + fn)
            sticker_output = StringIO()
            sticker.save(sticker_output, format='PNG')
            sticker_im_data = sticker_output.getvalue()
            sticker_img_str = 'data:image/png;base64,' + base64.b64encode(sticker_im_data)
        else:
            sticker_img_str = app.config['FAILEDIMG']

        order['sticker'] = sticker_img_str

        if os.path.isfile(app.config['LABELS_FOLDER'] + fn):
            label = Image.open(app.config['LABELS_FOLDER'] + fn)
            label_output = StringIO()
            label.save(label_output, format='PNG')
            label_im_data = label_output.getvalue()
            label_img_str = 'data:image/png;base64,' + base64.b64encode(label_im_data)
        else:
            label_img_str = app.config['FAILEDIMG']

        order['label'] = label_img_str

        responses.append(order)
    return json.dumps(responses)

@app.route('/archives', methods=['GET'])
def list_archives():
    skinlist = os.listdir(app.config['SKINS_FOLDER'])
    responses = []

    for fn in skinlist:
        # archive = nonextension.split('_')
        archive = extract_metadata(fn)

        if os.path.isfile(app.config['CHARACTERS_FOLDER'] + fn):
            character = Image.open(app.config['CHARACTERS_FOLDER'] + fn)
            character_output = StringIO()
            character.save(character_output, format='PNG')
            character_im_data = character_output.getvalue()
            character_img_str = 'data:image/png;base64,' + base64.b64encode(character_im_data)
        else:
            character_img_str = app.config['FAILEDIMG']

        archive['character'] = character_img_str

        skin = Image.open(app.config['SKINS_FOLDER'] + fn)
        skin_output = StringIO()
        skin.save(skin_output, format='PNG')
        skin_im_data = skin_output.getvalue()
        skin_img_str = 'data:image/png;base64,' + base64.b64encode(skin_im_data)
        archive['skin'] = skin_img_str

        if os.path.isfile(app.config['STICKERS_FOLDER'] + fn):
            sticker = Image.open(app.config['STICKERS_FOLDER'] + fn)
            sticker_output = StringIO()
            sticker.save(sticker_output, format='PNG')
            sticker_im_data = sticker_output.getvalue()
            sticker_img_str = 'data:image/png;base64,' + base64.b64encode(sticker_im_data)
        else:
            sticker_img_str = app.config['FAILEDIMG']

        archive['sticker'] = sticker_img_str

        if os.path.isfile(app.config['LABELS_FOLDER'] + fn):
            label = Image.open(app.config['LABELS_FOLDER'] + fn)
            label_output = StringIO()
            label.save(label_output, format='PNG')
            label_im_data = label_output.getvalue()
            label_img_str = 'data:image/png;base64,' + base64.b64encode(label_im_data)
        else:
            label_img_str = app.config['FAILEDIMG']

        archive['label'] = label_img_str

        responses.append(archive)
    return json.dumps(responses)

@app.route('/fulfill/<int:order_id>', methods=['POST'])
def fulfill_order(order_id):
    # Make sure the skin we're archiving is actually in the system
    skinlist = os.listdir(app.config['SKINS_FOLDER'])
    foundfile = ''
    for fn in skinlist:
        skin_metadata = extract_metadata(fn)
        if int(skin_metadata['id']) == order_id:
            foundfile = fn

    if foundfile:
        # Move this skin file into the archive folder
        origin = app.config['SKINS_FOLDER'] + foundfile
        destination = app.config['ARCHIVES_FOLDER'] + foundfile
        open(destination, "w").close()
        shutil.copy(origin, destination)
        return ('Success', 201)
    else:
        # Check if the file which user is trying to archive
        # was already archived.
        archivelist = os.listdir(app.config['ARCHIVES_FOLDER'])
        for fn in archivelist:
            archive = extract_metadata(fn)
            if archive['id'] == order_id:
                foundfile = fn;
                return ('Already archived', 409)
        if foundfile == '':
            return ('No such order', 422)

def extract_metadata(fn):
    fn_with_extension = fn.split('.')
    fn_nonextension = fn_with_extension[0]
    metadata = fn_nonextension.split('_')
    order = {}
    order['fn'] = fn
    order['id'] = int(metadata[0]) if len(metadata) > 0 else 0
    order['dt'] = metadata[1] if len(metadata) > 1 else 'missing date-time'
    order['item'] = metadata[2] if len(metadata) > 2 else '?'
    order['cn'] = metadata[3] if len(metadata) > 3 else 'Name not provided'
    return order

def list_files(folder):
    filelist = os.listdir(app.config[folder + '_FOLDER'])
    responses = []

    for fn in filelist:
        metadata = extract_metadata(fn)

        if os.path.isfile(app.config['CHARACTERS_FOLDER'] + fn):
            character = Image.open(app.config['CHARACTERS_FOLDER'] + fn)
            character_output = StringIO()
            character.save(character_output, format='PNG')
            character_im_data = character_output.getvalue()
            character_img_str = 'data:image/png;base64,' + base64.b64encode(character_im_data)
        else:
            character_img_str = app.config['FAILEDIMG']

        metadata['character'] = character_img_str

        skin = Image.open(app.config['SKINS_FOLDER'] + fn)
        skin_output = StringIO()
        skin.save(skin_output, format='PNG')
        skin_im_data = skin_output.getvalue()
        skin_img_str = 'data:image/png;base64,' + base64.b64encode(skin_im_data)
        metadata['skin'] = skin_img_str

        if os.path.isfile(app.config['STICKERS_FOLDER'] + fn):
            sticker = Image.open(app.config['STICKERS_FOLDER'] + fn)
            sticker_output = StringIO()
            sticker.save(sticker_output, format='PNG')
            sticker_im_data = sticker_output.getvalue()
            sticker_img_str = 'data:image/png;base64,' + base64.b64encode(sticker_im_data)
        else:
            sticker_img_str = app.config['FAILEDIMG']

        metadata['sticker'] = sticker_img_str

        if os.path.isfile(app.config['LABELS_FOLDER'] + fn):
            label = Image.open(app.config['LABELS_FOLDER'] + fn)
            label_output = StringIO()
            label.save(label_output, format='PNG')
            label_im_data = label_output.getvalue()
            label_img_str = 'data:image/png;base64,' + base64.b64encode(label_im_data)
        else:
            label_img_str = app.config['FAILEDIMG']

        metadata['label'] = label_img_str

        responses.append(metadata)
    return json.dumps(responses)
