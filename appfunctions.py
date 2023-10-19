import cdk8s_plus_25 as kplus
from cdk8s import App, Chart, Size, ApiObjectMetadata
import yaml


class Containerspec:
    def containerports(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            c_ports = (config['deployment']['container']['ports'])
            cports = []
            for port in c_ports:
                cports.append(kplus.ContainerPort(name=str(port['name']), number=int(port['containerPort'])))
        return (cports)

    def containerresources(self):
        with open(('config.yaml')) as y:
            config = yaml.safe_load(y)
            c_resources = (config['deployment']['container']['resources'])
            cpu = kplus.Cpu.millis
            mem = Size.mebibytes
            cpulim = int(c_resources['cpu']['limits'])
            cpureq = int(c_resources['cpu']['requests'])
            memlim = int(c_resources['memory']['limits'])
            memreq = int(c_resources['memory']['requests'])
            cpures = kplus.CpuResources(limit=cpu(cpulim), request=cpu(cpureq))
            memres = kplus.MemoryResources(limit=mem(memlim), request=mem(memreq))
            resources = kplus.ContainerResources(cpu=cpures, memory=memres)
        return (resources)


class Servicespec:

    def serviceports(self):
        with open('config.yaml') as y:
            config = yaml.safe_load(y)
            s_ports = (config['service']['ports'])
            sports = []
            for port in s_ports:
                sports.append(kplus.ServicePort(name=str(port['name']),
                                                port=int(port['port']),
                                                target_port=int(port['targetPort']),
                                                protocol=kplus.Protocol(str(port['protocol']))))
            return (sports)


class Ingressspec:

    def ingressannotations(self):
        with open(('config.yaml')) as y:
            config = yaml.safe_load(y)
            ingannotations = config['ingress']['annotations']
        return (ingannotations)

    def ingresshost(self):
        with open(('config.yaml')) as y:
            config = yaml.safe_load(y)
            inghost = str(config['ingress']['hostname'])
        return (inghost)

    def ingresstlshost(self):
        with open(('config.yaml')) as y:
            config = yaml.safe_load(y)
            tlsname = str(config['ingress']['hostname'])
            ingtlsname = [kplus.IngressTls(hosts=[tlsname])]
            return (ingtlsname)

    def ingressport(self):
        with open(('config.yaml')) as y:
            config = yaml.safe_load(y)
            ingport = config['ingress']['port']
        return (ingport)

    def ingresspath(self):
        with open(('config.yaml')) as y:
            config = yaml.safe_load(y)
            ingpass = str(config['ingress']['path'])
        return (ingpass)

