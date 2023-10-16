from cdk8s import App, Chart
from constructs import Construct
import cdk8s_plus_25 as kplus


class Application(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        namespace = kplus.Namespace(self, "app-namespace")
        deployment = kplus.Deployment(self, "deployment", containers=[kplus.ContainerProps(
            image='ubuntu',
            ports=[kplus.ContainerPort(name="http", number=80), kplus.ContainerPort(name="grpc", number=9999)])
        ])
        service = kplus.Service(self, "service",
                                ports=[kplus.ServicePort(name="http", port=80, target_port=80),
                                       kplus.ServicePort(name="grpc", port=9999, target_port=9999),
                                       kplus.ServicePort(name="metrics", port=9000, target_port=9000)])

        ingress = kplus.Ingress(self, "ingress", tls=[kplus.IngressTls(hosts=["app2.domain.com"])])
        ingress.add_host_rule(path="/", host="app2.domain.com", backend=kplus.IngressBackend.from_service(serv=service,
                                                                                                          port=80))


app = App()

Application(app, "app2")

app.synth()
