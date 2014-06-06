from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor, ssl, defer
from twisted.python import log
import sys, os, json

RELAY_PIN = 17

class RelayActivator(Resource):
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        try:
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            reactor.callLater(1, GPIO.output, RELAY_PIN, GPIO.LOW)
        except NameError:
            pass
        return json.dumps({ 'success': True })


def create_static_child(file):
    file.putChild('static', File('static'))

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    control = File('control')
    create_static_child(control)
    control.putChild('fire', RelayActivator())
    reactor.listenTCP(80, Site(control))

    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
    except ImportError:
        log.err()

    reactor.run()