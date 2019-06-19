import zbar

from PIL import Image
import cv2
from pyzbar.pyzbar import decode
#import Gate_BC


def main_j():
    """
    A simple function that captures webcam video utilizing OpenCV. The video is then broken down into frames which
    are constantly displayed. The frame is then converted to grayscale for better contrast. Afterwards, the image
    is transformed into a numpy array using PIL. This is needed to create zbar image. This zbar image is then scanned
    utilizing zbar's image scanner and will then print the decodeed message of any QR or bar code. To quit the program,
    press "q".
    :return:
    """

    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture(0)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Displays the current frame
        cv2.imshow('Current', frame)

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)
        test_decode = decode(image)

        # Prints data from image.
        for decoded in zbar_image:
            tx_hash = decoded.data
            print(tx_hash)
            print(test_decode[0].data)
            break
            '''if Gate_BC.validate(tx_hash):
                print('O')
                #open Gate
            else:
                print('e')
                # rasise Error
            print(decoded.data)'''


def capture_qr():
    cap = cv2.VideoCapture(1)
    token_before = 'Null2'
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        cv2.rectangle(frame, (100, 100), (200, 200), [255, 0, 0], 2)
        cv2.imshow('Current',frame)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        #image.tobytes()
        qr_decode = decode(image)
        token = 'NULL'
        if qr_decode:
            #time.sleep(3)
            token = qr_decode[0].data
            token = token.decode('utf-8')
            if token != token_before :
                token_before = token
                print(token)
                auth(token)

capture_qr()