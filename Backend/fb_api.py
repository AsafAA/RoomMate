import socket, ssl, json, struct
import binascii

def send_push_notification(thePayLoad,device_token):
    try:
        deviceToken = db.get_device_token(fb_token)
        theCertfile = 'cert_ios_production.pem'
        theHost = ( 'gateway.push.apple.com', 2195 )
        data = json.dumps( thePayLoad )
        deviceToken = deviceToken.replace(' ','')
        byteToken = binascii.unhexlify(deviceToken)
        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack( theFormat, 0, 32, byteToken, len(data), data )
        ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = theCertfile )
        ssl_sock.connect( theHost )
        ssl_sock.write( theNotification )
        ssl_sock.close()
        return True
    except Exception:
        return False
