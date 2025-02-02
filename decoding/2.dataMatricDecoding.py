import pyzxing

reader = pyzxing.BarCodeReader()

# Decode the image
barcode = reader.decode('decoding/datamatrix_code.jpg')

if barcode:
    print("Decoded Data:", barcode[0]['raw'])
else:
    print("No Data Matrix code found.")
