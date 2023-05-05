from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecsp,
    aws_ecr_assets as ecr_assets,
)
from constructs import Construct
from dotenv import dotenv_values


class PythonCdkBoilerplateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        asset = ecr_assets.DockerImageAsset(self, 'DockerImageAsset', directory='.')

        vpc = ec2.Vpc(
            self, 'Vpc',
            max_azs=2,
            subnet_configuration=[ec2.SubnetConfiguration(name='public', subnet_type=ec2.SubnetType.PUBLIC)]
        )

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc, enable_fargate_capacity_providers=True)

        task_definition = ecs.FargateTaskDefinition(self, 'FargateTaskDefinition', cpu=1024, memory_limit_mib=3072)
        task_definition.add_container(
            'web',
            image=ecs.ContainerImage.from_docker_image_asset(asset),
            port_mappings=[ecs.PortMapping(container_port=80, protocol=ecs.Protocol.TCP)],
            environment=dotenv_values('.env'),
        )

        service = ecsp.ApplicationLoadBalancedFargateService(
            self, 'ApplicationLoadBalancedFargateService',
            cluster=cluster,
            task_definition=task_definition,
            capacity_provider_strategies=[
                ecs.CapacityProviderStrategy(capacity_provider='FARGATE', weight=1, base=0)
            ],
            assign_public_ip=True,
        )
        service.target_group.configure_health_check(path='/health')
