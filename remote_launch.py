from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor, ssl
from twisted.python import log
import sys, os, json

RELAY_PIN = 17

SSL_ROOT = 'ssl'
sslContext = ssl.DefaultOpenSSLContextFactory(
    os.path.join(SSL_ROOT, 'key.pem'),
    os.path.join(SSL_ROOT, 'certificate.crt'),
)

class RelayActivator(Resource):
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        reactor.callLater(0, GPIO.output, RELAY_PIN, GPIO.HIGH)
        reactor.callLater(1, GPIO.output, RELAY_PIN, GPIO.LOW)
        return json.dumps({ 'success': True })


def create_static_child(file):
    file.putChild('static', File('static'))

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    facade = File('facade')
    create_static_child(facade)
    facade.putChild('certificate.crt', File(os.path.join(SSL_ROOT, 'certificate.crt')))
    reactor.listenTCP(80, Site(facade))

    control = File('control')
    create_static_child(control)
    control.putChild('fire', RelayActivator())
    reactor.listenSSL(443, Site(control), contextFactory=sslContext,)

    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
    except ImportError:
        log.err()

    reactor.run()