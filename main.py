from cdk8s import App, Chart, Size
from constructs import Construct
import cdk8s_plus_25 as kplus

app_name = input("enter application name ")


class Application(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        ns = input("enter namespace ")
        namespace = kplus.Namespace(self, ns)
        image_name = input("enter image name ")
        def container_port():
            print("prepare deployment ports")
            i = int(input("set container port count  "))
            c = []
            while i > 0:
                cname = input("enter container port name  ")
                cport = int(input("enter port "))
                c.append(kplus.ContainerPort(name=cname, number=cport))
                i = i - 1
            return c

        cpu = kplus.Cpu.millis
        mem = Size.mebibytes
        cpures = kplus.CpuResources(limit=cpu(int(input("enter cpu limit "))), request=cpu(int(input("enter cpu requests "))))
        memres = kplus.MemoryResources(limit=mem(int(input("enter memory limit "))), request=mem(int(input("enter memory requests "))))

        deployment = kplus.Deployment(self, "deployment")
        deployment.add_container(image=image_name, name=app_name, ports=container_port(),
                                 resources=(kplus.ContainerResources(cpu=cpures, memory=memres))
                                 )

        def service_port():
            print("prepare service ports")
            i = int(input("set service port count  "))
            s = []
            while i > 0:
                sname = input("enter service port name  ")
                sport = int(input("enter service port "))
                stargetport = int(input("enter target port  "))
                s.append(kplus.ServicePort(name=sname, port=sport, target_port=stargetport, protocol=kplus.Protocol("TCP")))
                i = i - 1
            return s

        service = kplus.Service(self, "service", ports=service_port())

        ingresscheck = input("create ingress? yes or no  ")

        hostname = app_name + ".domain.com"


        if ingresscheck == "yes":
            hostnamecheck = input("are you want change standard hostname?  yes or no ")
            if hostnamecheck == "yes":
                hostname = input("enter hostname ")
            ingress = kplus.Ingress(self, "ingress", tls=[kplus.IngressTls(hosts=[hostname])])
            ingress.add_host_rule(path="/", host=hostname,
                                  backend=kplus.IngressBackend.from_service(serv=service,
                                                                            port=int(input("input ingress port "))))


app = App()

Application(app, app_name)

app.synth()
