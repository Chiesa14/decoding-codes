import os
from pyzxing import BarCodeReader

reader = BarCodeReader()
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'image-03-barcode.jpg')
barcodes = reader.decode(image_path)
if barcodes:
    for barcode in barcodes:
        print(f'Decoded data: {barcode["raw"]}')
        print(f'Barcode format: {barcode["format"]}')
else:
    print('No barcode detected.')
