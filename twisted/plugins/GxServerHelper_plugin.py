#coding: utf-8

from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import service, internet
from twisted.internet import protocol

from GxServer import util,server
import txmongo

class Options(usage.Options):
  optParameters = [
      ["config","c","config/pcrf.conf","configuration file"],
      ]


class ServiceMaker(object):
  implements(service.IServiceMaker, IPlugin)
  tapname = "GxServerHelper"
  description = "SV Lab Helper"
  options = Options

  def makeService(self,options):
    config = util.parse_config(options['config'])
    s = service.MultiService()
    mongo = txmongo.lazyMongoConnectionPool(host=config.mongo_host,
        port=config.mongo_port,pool_size=config.mongo_pool_size)

    i = internet.TCPServer(config.server_port,
        server.Application(config,mongo),interface=config.server_host)

    i.setServiceParent(s)

    return s

serviceMaker = ServiceMaker()