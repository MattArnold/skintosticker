from app import app, SkinToSticker
from flask import request, json, abort
import os, base64, urllib
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
            svgname = '%s_%s_%d.svg' % (order_id, dt, i)
            properties = item['properties']

            # Save the preview image
            character = properties[1]['value'][22:] # properties[1] will be the preview image
            characterpath = os.path.join(app.config['CHARACTERS_FOLDER'], fname)
            characterfh = open(characterpath, 'wb')
            characterfh.write(character.decode('base64'))
            characterfh.close()

            # Save the original skin
            skin = properties[0]['value'][22:] # properties[0] will be the skin
            skinpath = os.path.join(app.config['SKINS_FOLDER'], fname)
            skinfh = open(skinpath, 'wb')
            skinfh.write(skin.decode('base64'))
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

    # Create an SVG file to print the character and shipping label
    # precisely within the vinyl-cutter paths.
    svg_template = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="792px" height="612px" viewBox="0 0 792 612" enable-background="new 0 0 792 612" xml:space="preserve"><image overflow="visible" x="18.5" y="55" width="609.572" height="502" xlink:href="' + sticker_path + '"></image><image overflow="visible" x="630" y="198" width="144" height="216" xlink:href="' + label_path + '"></image><text transform="matrix(1 0 0 1 630 30)" font-family="Arial" font-size="12">name:</text><text transform="matrix(1 0 0 1 630 50)" font-family="Arial" font-size="12">princess_flutter</text></svg>'
    final_path = os.path.join(app.config['FINALS_FOLDER'], svgname)
    printable_file = open(final_path, 'w')
    printable_file.write(svg_template)
    printable_file.close()

    return ('Success', 201)

@app.route('/orders', methods=['GET'])
def list_orders():
    skinlist = os.listdir(app.config['SKINS_FOLDER'])
    responses = []
    failedimg = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIIAAACCCAIAAAAFYYeqAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDE0IDc5LjE1MTQ4MSwgMjAxMy8wMy8xMy0xMjowOToxNSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo3MDYzMjVBRUM3QkQxMUU0OTEyRUFDN0M0RUJCMkNFOCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo3MDYzMjVBRkM3QkQxMUU0OTEyRUFDN0M0RUJCMkNFOCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjcwNjMyNUFDQzdCRDExRTQ5MTJFQUM3QzRFQkIyQ0U4IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjcwNjMyNUFEQzdCRDExRTQ5MTJFQUM3QzRFQkIyQ0U4Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+X1XKtQAABh9JREFUeNrsnW1P8kwQ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'

    for fn in skinlist:
    	withextension = fn.split('.')
    	nonextension = withextension[0]
    	metadata = nonextension.split('_')
        order = {}
        order['fn'] = fn
        order['id'] = metadata[0]
        order['dt'] = metadata[1]
        order['item'] = metadata[2]

        if os.path.isfile(app.config['CHARACTERS_FOLDER'] + fn):
            character = Image.open(app.config['CHARACTERS_FOLDER'] + fn)
            character_output = StringIO()
            character.save(character_output, format='PNG')
            character_im_data = character_output.getvalue()
            character_img_str = 'data:image/png;base64,' + base64.b64encode(character_im_data)
        else:
            character_img_str = failedimg

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
            sticker_img_str = failedimg

        order['sticker'] = sticker_img_str

        if os.path.isfile(app.config['LABELS_FOLDER'] + fn):
            label = Image.open(app.config['LABELS_FOLDER'] + fn)
            label_output = StringIO()
            label.save(label_output, format='PNG')
            label_im_data = label_output.getvalue()
            label_img_str = 'data:image/png;base64,' + base64.b64encode(label_im_data)
        else:
            label_img_str = failedimg

        order['label'] = label_img_str

        responses.append(order)
    return json.dumps(responses)
