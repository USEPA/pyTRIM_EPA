# webTRIM.FaTE AWS Infrastructure & Deployment

This directory contains all AWS infrastructure automation using CloudFormation and deployment tooling for the webTRIM.FaTE application.

## Overview

The AWS stack provisions a multi-tier application on AWS with:
- **Database Tier**: RDS (PostgreSQL or MySQL)
- **Compute Tier**: Elastic Beanstalk for the Flask web application
- **Model Execution**: ECS Fargate clusters for model-run and getflow Docker containers
- **Step Functions**:  State machines for async model execution
- **Storage**: S3 buckets for model outputs and scenario files
- **Container Registry**: ECR repositories for Docker images
- **Networking**: VPC with public/private subnets, NAT gateways, security groups, and bastion host

## Prerequisites

### Tooling

- **AWS CLI v2** with valid credentials configured
- **Python 3.11+** with deployment dependencies:
  ```bash
  pip install -r requirements.txt  # Installs boto3, etc.
  ```
- **Docker** (for building and pushing model containers)
- **AWS SSO** or IAM credentials with sufficient permissions (see IAM Permissions)

### AWS Account Setup

1. **Create or use an existing AWS account** with the desired region (default: us-east-1).
2. **Configure AWS CLI**:
   ```bash
   aws configure
   # or if using AWS SSO:
   aws sso login --profile your-profile
   ```
3. **Generate or import an SSH keypair** (used for bastion host access and EC2 instances):
   ```bash
   aws ec2 create-key-pair --key-name pytrim-dev-keypair-<date> --query 'KeyMaterial' --output text > ~/.ssh/pytrim-dev.pem
   chmod 600 ~/.ssh/pytrim-dev.pem
   ```

## Configuration

### Environment Presets

webTRIM.FaTE supports multiple deployment environments (dev, staging, prod, etc.).

**Example: iac/dev.json**

```json
{
  "environment_name": "trim-dev",
  "short_env_profile": "dev",
  "aws": {
    "ssh_keypair_name": "trim-dev-keypair-20260528",
    "eip_name": "trim-dev-eip",
    "webserver_certificate_id": "c554f7ce-4d87-4ad6-9742-cb4de4a4e729",
    "cidr_segment_vpc": 24,
    "ec2_ingress": [
      {
        "description": "VPN",
        "cidr": "199.123.45.0/24"
      }
    ],
    "db": {
      "dbname": "trimdb",
      "username": "trim_user",
      "password": "redacted_password_here"
    }
  }
}
```

**Configuration Fields:**

| Field | Description | Example |
|-------|-------------|---------|
| `environment_name` | Unique name for the CloudFormation stack and AWS resources | `trim-dev` |
| `short_env_profile` | Short profile name (dev, staging, prod) | `dev` |
| `aws.ssh_keypair_name` | EC2 SSH keypair name (must exist in AWS) | `trim-dev-keypair-20260528` |
| `aws.eip_name` | Name for the Elastic IP allocation (for bastion/web tier) | `trim-dev-eip` |
| `aws.webserver_certificate_id` | ACM certificate ID for HTTPS (must exist in AWS) | `c554f7ce-4d87-4ad6-9742-cb4de4a4e729` |
| `aws.cidr_segment_vpc` | Third octet of VPC CIDR block (e.g., 24 → 10.24.0.0/16) | `24` |
| `aws.ec2_ingress` | List of CIDR blocks allowed SSH access to bastion | `[{description, cidr}]` |
| `aws.db.dbname` | RDS database name | `trimdb` |
| `aws.db.username` | RDS master username | `trim_user` |
| `aws.db.password` | RDS master password (8+ characters) | `redacted_password_here` |
| `aws.crons` | Optional scheduled EC2 capacity scaling | See below |

**Cron Jobs (optional):**

Define EC2 auto-scaling schedules to reduce costs:

```json
"crons": {
  "ec2": [
    {
      "name": "weekday_startup",
      "cron_expression": "0 8 * * MON-FRI",  # 8 AM Mon-Fri (UTC)
      "capacity": 1  # Scale up to 1 instance
    },
    {
      "name": "weekday_shutdown",
      "cron_expression": "0 18 * * MON-FRI",  # 6 PM Mon-Fri (UTC)
      "capacity": 0  # Scale down to 0 instances
    }
  ]
}
```

### Creating a New Environment

1. **Copy an existing config**:
   ```bash
   cp iac/dev.json iac/my-environment.json
   ```

2. **Update all fields**:
   - `environment_name`: Must be unique across your AWS account.
   - `ssh_keypair_name`: Create the keypair if it doesn't exist.
   - `eip_name`: Choose a unique name.
   - `webserver_certificate_id`: Request or import an ACM certificate if needed.
   - `db.password`: Use a strong, unique password.
   - `ec2_ingress`: Update CIDR blocks for your network.

## Deployment

### Deployment Modes

The deployment script (pytrim_deploy.py) supports modular deployment via the `-m` (mode) flag:

| Mode | Description |
|------|-------------|
| `full` | Deploy everything: SSH key, EIP, CloudFormation stack, Docker images, and Elastic Beanstalk. |
| `ssh_key` | Create or verify SSH keypair. |
| `elastic_ip` | Allocate or verify Elastic IP. |
| `cloudformation` | Create or update the CloudFormation stack. |
| `docker` | Build and push Docker images (model-run and/or getflow). |
| `push_flask_build` | Package and deploy Flask app to Elastic Beanstalk. |
| `crons` | Set up cron job triggers for EC2 auto-scaling. |

### Basic Deployment

**Deploy a new environment:**

```bash
cd iac
python src/deployer/pytrim_deploy.py -c dev.json -m full -p your-aws-profile
```

You will be prompted:
```
Running PyTrim deployment script, mode 'full', as AWS userid 'AIDAI...' on account '123456789012'
Proceed [y/n]? y
```

**Deploy only Docker images (after code changes):**

```bash
python src/deployer/pytrim_deploy.py -c dev.json -m docker -d runmodel
# or:
python src/deployer/pytrim_deploy.py -c dev.json -m docker -d getflow
# or both:
python src/deployer/pytrim_deploy.py -c dev.json -m docker
```

**Deploy only the Flask web app:**

```bash
python src/deployer/pytrim_deploy.py -c dev.json -m push_flask_build -p your-aws-profile
```

**Deploy or update CloudFormation stack:**

```bash
python src/deployer/pytrim_deploy.py -c dev.json -m cloudformation -p your-aws-profile
```

### Deployment Script Options

```
python src/deployer/pytrim_deploy.py -c <config_file> [-m <mode>] [-p <aws_profile>] [-d <docker_mode>]

Options:
  -c, --config        Path to environment config JSON (required)
  -m, --mode          Deployment mode (default: full)
  -p, --profile       AWS profile name (for credential resolution)
  -d, --docker        Docker build mode (runmodel, getflow, or both)
```

## AWS Resources Created

The CloudFormation template (src/cloudformation/pytrim.yaml) provisions:

### Networking
- **VPC**: Custom VPC with CIDR block `10.{cidr_segment}.0.0/16`
- **Subnets**: 
  - 2 public subnets (for ALB, Bastion, NAT Gateway)
  - 2 private subnets (for RDS, ECS tasks)
  - 2 RDS-specific private subnets
- **Security Groups**: Separate groups for web tier, RDS, model execution, and bastion
- **NAT Gateway**: For private subnet outbound internet access
- **Bastion Host**: EC2 instance for SSH tunneling to private resources (optional via AWS CloudFormation template)

### Database
- **RDS Instance**: 
  - Supports MySQL or PostgreSQL (configurable)
  - 100 GB storage (configurable)
  - 7-day backup retention
  - Multi-AZ deployment for high availability
  - Allocated storage, instance class, and engine version are configurable
- **Secrets Manager Secret**: Stores database credentials (`pytrim/database/credentials`)

### Container Orchestration
- **ECR Repositories**:
  - `{environment_name}/private_ecr_repo_modelrun`: For model-run image
  - `{environment_name}/private_ecr_repo_getflow`: For getflow image
- **ECS Clusters**:
  - `{environment_name}_container_cluster_modelrun`: For model execution
  - `{environment_name}_container_cluster_getflow`: For getflow execution
- **ECS Task Definitions**:
  - Model-run task: 16 vCPU, 72 GB RAM (configurable in template)
  - GetFlow task: 8 vCPU, 32 GB RAM (configurable in template)
- **Step Functions State Machines**:
  - `{environment_name}-dockerized-runmodel-statemachine`: Triggers model-run ECS tasks
  - `{environment_name}-dockerized-getflow-statemachine`: Triggers getflow ECS tasks

### Storage
- **S3 Buckets**:
  - `{environment_name}-model-run-storage-bucket`: Model execution outputs
  - `{environment_name}-getflow-storage-bucket`: GetFlow outputs
  - `{environment_name}-scenario-miscfiles-bucket`: User scenario files, with CORS enabled for web access

### Web Tier
- **Elastic Beanstalk Application**: Hosts Flask web application
- **Elastic Beanstalk Environment**: Auto-scaling EC2 instances running Python 3.11
  - Platform: `64bit Amazon Linux 2023 v4.13.1 running Python 3.11` (see note below)
  - Supports custom domain and HTTPS via ACM certificate
  - Auto-scaling based on CPU/network metrics

### IAM Roles & Policies
- **DockerTaskExecutionRole**: Allows ECS tasks to pull images and write logs
- **DockerTaskTaskRole**: Allows ECS tasks to access S3, Secrets Manager, and Step Functions
- **StepFunctionAssumedRole**: Allows Step Functions to invoke ECS tasks
- **Bastion Role**: Allows bastion host to manage VPC and SSM Session Manager

## Important Notes

### EB Platform Version

The CloudFormation template specifies a hard-coded Elastic Beanstalk platform version:

```yaml
SolutionStackName: '64bit Amazon Linux 2023 v4.13.1 running Python 3.11'
```

If AWS discontinues this platform version, update the template to a newer version. Check available versions:

```bash
aws elasticbeanstalk describe-platform-versions --filters Type=PlatformOperatingSystemName,Values="Amazon Linux 2023" --query 'PlatformSummaryList[*].PlatformArn'
```

### Docker Image Architecture

Model-run and getflow containers are built with `--platform linux/amd64` to ensure compatibility on AWS Fargate (which uses x86-64). On non-x86 development machines (e.g., Apple Silicon), you may need to use `docker buildx` or push pre-built images from an x86 builder.

### Secrets Manager

Database credentials are stored in AWS Secrets Manager under the key `pytrim/database/credentials`. The ECS tasks retrieve credentials from this secret at runtime. Update the secret if you change the database password:

```bash
aws secretsmanager update-secret \
  --secret-id pytrim/database/credentials \
  --secret-string '{"username":"pytrim_user","password":"new_password_here"}'
```

## Monitoring & Logs

### CloudWatch Logs

- **ECS Model-Run Tasks**: `/ecs/pytrim_sample_taskdef`
- **ECS GetFlow Tasks**: `/ecs/pytrim_getflow_taskdef`
- **Elastic Beanstalk**: Check via AWS Elastic Beanstalk console or:
  ```bash
  aws elasticbeanstalk retrieve-environment-info --environment-name trim-dev-web --info-type logs
  ```

### Step Functions

Monitor model execution via Step Functions console:

```bash
aws stepfunctions list-executions \
  --state-machine-arn arn:aws:states:us-east-1:123456789012:stateMachine:trim-dev-dockerized-runmodel-statemachine
```

## IAM Permissions

IAM permissions required for deployment (create an IAM policy):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "ec2:*",
        "rds:*",
        "s3:*",
        "ecr:*",
        "ecs:*",
        "elasticbeanstalk:*",
        "steps:*",
        "iam:*",
        "logs:*",
        "secretsmanager:*",
        "acm:*"
      ],
      "Resource": "*"
    }
  ]
}
```

For production, restrict Resource ARNs to specific resources.

## Cleanup

To delete a deployment and all associated AWS resources:

```bash
python src/deployer/pytrim_deploy.py -c dev.json -m cloudformation -p your-aws-profile
# Then use AWS CloudFormation console or CLI to delete the stack:
aws cloudformation delete-stack --stack-name trim-dev
```

**Warning**: This will delete the RDS database and S3 buckets. Ensure all critical data is backed up first.

## Support

For issues related to specific AWS services, refer to:
- **CloudFormation**: [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)
- **ECS/Fargate**: [ECS Documentation](https://docs.aws.amazon.com/ecs/)
- **RDS**: [RDS Documentation](https://docs.aws.amazon.com/rds/)
- **Elastic Beanstalk**: [Elastic Beanstalk Documentation](https://docs.aws.amazon.com/elasticbeanstalk/)

For application-specific issues, see the main README.md.
