import RPi.GPIO as GPIO
import sys
import time
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

LED_1 = 17
LED_2 = 18
LED_3 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(LED_2, GPIO.OUT)
GPIO.setup(LED_3, GPIO.OUT)

Port = 9000

LED_r = 'OFF'
LED_g = 'OFF'
LED_b = 'OFF'

style = ('<style>'
         'body {'
         '    font-family: Arial, sans-serif;'
         '    text-align: center;'
         '}'
         'table {'
         '    margin: auto;'
         '    border-collapse: collapse;'
         '}'
         'th, td {'
         '    padding: 10px;'
         '    border: 1px solid black;'
         '}'
         'input {'
         '   margin: 10px;'
         '    padding: 10px;'
         '    font-size: 20px;'
         '    color: white;'
         '    border: none;'
         '    border-radius: 10px;'
         '    box-shadow: 2px 2px 5px gray;'
         '}'
         'input:hover {'
         '    box-shadow: none;'
         '}'
         'input.active {'
         '    box-shadow: inset 2px 2px 5px gray;'
         '}'
         '.green {'
         '    background-color: limegreen;'
         '}'
         '.red {'
         '    background-color: crimson;'
         '}'
         '.blue {'
         '    background-color: dodgerblue;'
         '}'
         '</style>')

table1 = '''
    <h1>LED Control</h1>
    <p>Click the buttons below to turn on or off the LEDs.</p>
    <form action="/handle_form" method="post">
        <table>
            <tr>
                <td> Green LED </td>
                <td><input id="green" class="green" name="g_btn" type="submit" value=%s></td>
            </tr>
            <tr>
                <td> Red LED </td>
                <td><input id="red" class="red" name="r_btn" type="submit" value=%s></td>
            </tr>
            <tr>
                <td> Blue LED </td>
                <td><input id="blue" class="blue" name="b_btn" type="submit" value=%s></td>
            </tr>
        </table>
    </form>
'''

table2 = '''
    <h1>LED Control</h1>
    <p>Click the buttons below to turn on or off the LEDs.</p>
    <form action="/handle_form" method="post">
       <div class="container">
	   <div class="row">
	       <div class="col-sm-4">
		   <label for="green">Green LED</label>
		   <input id="green" class="btn btn-success" name="g_btn" type="submit" value=%s>
	       </div>
	       <div class="col-sm-4">
		   <label for="red">Red LED</label>
		   <input id="red" class="btn btn-danger" name="r_btn" type="submit" value=%s>
	       </div>
	       <div class="col-sm-4">
		   <label for="blue">Blue LED</label>
		   <input id="blue" class="btn btn-primary" name="b_btn" type="submit" value=%s>
	       </div>
	   </div>
      </div>
   </form>

'''

RES1 = ('<html><head><title>LED Control</title>%s</head><body>%s</body></html>')

RES2 = '''
   <html>
   <head>
       <title>LED Control</title>
       <meta charset="utf-8">
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
       <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
   </head>
   <body>
       <div class="container">
	   <h1 class="text-center">LED Control</h1>
	   <p class="text-center">Click the buttons below to turn on or off the LEDs.</p>
	   %s
       </div>
   </body>
   </html>

'''

body_content = ''


class LED_Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            #body_content = table1 % (LED_g, LED_r, LED_b,)
            body_content = table2 % (LED_g, LED_r, LED_b,)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            #self.wfile.write(bytes(RES1 % (style, body_content,), "utf-8"))
            self.wfile.write(bytes(RES2 % (body_content,), "utf-8"))
        except:
            self.send_error(404, f"{sys.exc_info()[0]}")

    def do_POST(self):
        global LED_b, LED_r, LED_g
        try:
            content_length = int(self.headers['Content-Length'])
            form_data = self.rfile.read(content_length)

            # parse the form data into a dictionary
            form_data = parse_qs(form_data.decode())

            if 'g_btn' in form_data:
                LED_g = 'On' if LED_g == 'OFF' else 'OFF'
                state = GPIO.HIGH if LED_g == 'On' else GPIO.LOW
                GPIO.output(LED_1, state)
                time.sleep(0.1)
            elif 'r_btn' in form_data:
                LED_r = 'On' if LED_r == 'OFF' else 'OFF'
                state = GPIO.HIGH if LED_r == 'On' else GPIO.LOW
                GPIO.output(LED_2, state)
                time.sleep(0.1)
            elif 'b_btn' in form_data:
                LED_b = 'On' if LED_b == 'OFF' else 'OFF'
                state = GPIO.HIGH if LED_b == 'On' else GPIO.LOW
                GPIO.output(LED_3, state)
                time.sleep(0.1)

            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

        except:
            self.send_error(404, f"{sys.exc_info()[0]}")


myServer = HTTPServer(("localhost", Port), LED_Handler)
try:
    myServer.serve_forever()
except KeyboardInterrupt:
    myServer.server_close()
    GPIO.cleanup()