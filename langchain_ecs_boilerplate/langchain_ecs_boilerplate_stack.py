from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecsp,
    aws_ecr_assets as ecr_assets,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_iam as iam
)
from constructs import Construct
from dotenv import dotenv_values

from src.create_index import DB_DIR

INDEX_BUCKET = 'langchain-ecs-boilerplate-index'


class LangchainEcsBoilerplateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        asset = ecr_assets.DockerImageAsset(self, 'DockerImageAsset', directory='.')

        vpc = ec2.Vpc(
            self, 'Vpc',
            max_azs=2,
            subnet_configuration=[ec2.SubnetConfiguration(name='public', subnet_type=ec2.SubnetType.PUBLIC)]
        )

        bucket = s3.Bucket(
            self, 'Bucket',
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            bucket_name=INDEX_BUCKET,
            removal_policy=RemovalPolicy.DESTROY,
            versioned=True,
        )
        s3_deployment.BucketDeployment(
            self, 'BucketDeployment',
            sources=[s3_deployment.Source.asset(DB_DIR)],
            destination_bucket=bucket,
        )

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc, enable_fargate_capacity_providers=True)

        task_definition = ecs.FargateTaskDefinition(self, 'FargateTaskDefinition', cpu=1024, memory_limit_mib=3072)
        task_definition.add_container(
            'app',
            image=ecs.ContainerImage.from_docker_image_asset(asset),
            port_mappings=[ecs.PortMapping(container_port=80, protocol=ecs.Protocol.TCP)],
            environment=dotenv_values('.env'),
            logging=ecs.LogDriver.aws_logs(stream_prefix='langchain-ecs-boilerplate')
        )
        task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:ListBucket"],
                resources=[bucket.bucket_arn]
            )
        )
        task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[f'{bucket.bucket_arn}/*']
            )
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
