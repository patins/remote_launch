from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
import sys, os, json

RELAY_PIN = 4

class RelayActivator(Resource):
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        try:
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            reactor.callLater(10, GPIO.output, RELAY_PIN, GPIO.LOW)
        except NameError:
            pass
        return json.dumps({ 'success': True })

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    control = File('static')
    control.putChild('fire', RelayActivator())
    reactor.listenTCP(80, Site(control))

    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
    except ImportError:
        log.err()

    reactor.run()

    try:
        GPIO.cleanup()
    except NameError:
        pass
