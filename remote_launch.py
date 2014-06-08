from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
import sys, os, json, config

class PingPong(Resource):
    def render_GET(self, request):
        request.setHeader("content-type", "text")
        return 'pong'

class RelayActivator(Resource):
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        try:
            GPIO.output(config.RELAY_PIN, GPIO.HIGH)
            reactor.callLater(10, GPIO.output, config.RELAY_PIN, GPIO.LOW)
        except NameError:
            pass
        return json.dumps({ 'success': True })

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    control = File('static')
    control.contentTypes['.manifest'] = 'text/cache-manifest'
    control.putChild('ping', PingPong())
    control.putChild('fire', RelayActivator())
    reactor.listenTCP(80, Site(control), interface=config.INTERFACE)

    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.RELAY_PIN, GPIO.OUT)
    except ImportError:
        log.err()

    reactor.run()

    try:
        GPIO.cleanup()
    except NameError:
        pass
