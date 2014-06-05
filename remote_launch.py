from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor, ssl

import os, json

SSL_ROOT = 'ssl'
sslContext = ssl.DefaultOpenSSLContextFactory(
    os.path.join(SSL_ROOT, 'key.pem'),
    os.path.join(SSL_ROOT, 'certificate.crt'),
)

class RelayActivator(Resource):
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        # TODO activate the relay
        return json.dumps({ 'success': True })


def create_static_child(file):
    file.putChild('static', File('static'))

if __name__ == '__main__':
    facade = File('facade')
    create_static_child(facade)
    facade.putChild('certificate.crt', File(os.path.join(SSL_ROOT, 'certificate.crt')))
    reactor.listenTCP(80, Site(facade))

    control = File('control')
    create_static_child(control)
    control.putChild('fire', RelayActivator())
    reactor.listenSSL(443, Site(control), contextFactory=sslContext,)

    reactor.run()