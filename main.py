from cdk8s import App, Chart, Size
from constructs import Construct
import cdk8s_plus_25 as kplus
import cdk8s
import yaml
from appfunctions import *


class Application(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        namespace = kplus.Namespace(self, "app-namespace")
        deployment = kplus.Deployment(self, "deployment")
        deployment.add_container(image="ubuntu",
                                 name="app3",
                                 resources=containerresources(),
                                 ports=containerports()
                                 )
        
        service = kplus.Service(self, "service",
                                ports=serviceports())
        ingressspec = Ingressspec()
        meta = cdk8s.ApiObjectMetadata(annotations=ingressspec.ingressannotations())
        ingress = kplus.Ingress(self, "ingress", tls=ingressspec.ingresstlshost(), metadata=meta)
        ingress.add_host_rule(path=ingressspec.ingresspath(),
                              host=ingressspec.ingresshost(),
                              backend=kplus.IngressBackend.from_service(serv=service, port=ingressspec.ingressport()))


app = App()

Application(app, "app4")

app.synth()
