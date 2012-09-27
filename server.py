'''
@author: Rodolfo Puig <Rodolfo.Puig@nbcuni.com>
@copyright: Telemundo Digital Media
@organization: NBCUniversal
'''

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, Application
from os.path import exists
from yaml import load
from app import runtime
from optparse import OptionParser

handler = WSGIContainer(runtime)
parser = OptionParser(usage='usage: %prog [options] dest')
parser.add_option('-c', '--config', dest='config', default='config.yaml', type='string', help='YAML configuration file (default: config.yaml)')
(options, args) = parser.parse_args()

if not exists(options.config):
    parser.error('the configuration file %s does not exist.' % options.config)

''' parse configuration file '''
fh = open(options.config)
config = load(fh)
fh.close()
if 'server' not in config:
    parser.error('%s is missing the "server" tree root' % options.config)
if 'host' not in config['server']:
    config['server']['host'] = '0.0.0.0'
if 'port' not in config['server']:
    config['server']['port'] = 8080

application = Application([
    (r".*", FallbackHandler, dict(fallback=handler))
])

if __name__ == "__main__":
    application.listen(config['server']['port'], config['server']['host'])
    IOLoop.instance().start()