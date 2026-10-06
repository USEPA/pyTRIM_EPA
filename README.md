# webTRIM.FaTE

This README provides a technical-level overview of the webTRIM.FaTE application.
For a user-oriented guide, see the [Quick Start Guide](Documentation/QSGuide_webTRIMFaTE.docx).

## Quick Links

- **Local Setup**: See [Local Development](#local-development)
- **Docker & Model Execution**: See [Docker](#docker)
- **AWS Deployment & Infrastructure**: See [iac/README.md](iac/README.md)

## Prerequisites

### Software Requirements

- **Python 3.11** (see [Pipfile](Pipfile))
- **pip** and **virtualenv** (or pipenv)
- **Docker** and **Docker Compose** (for Model-Run and GetFlow containers)
- **AWS CLI v2** and valid AWS credentials (for deployment and S3 access)
- **git** (for cloning and submodules if applicable)

### Runtime Dependencies

Core runtime packages:
- **Flask ecosystem**: Flask, Flask-SQLAlchemy, Flask-Security, Flask-Admin, Flask-Assets
- **Database drivers**: psycopg (PostgreSQL) or PyMySQL (MySQL)
- **AWS**: boto3, botocore
- **Data science**: pandas, numpy, scipy, matplotlib
- **Geospatial**: geopandas, shapely, pyproj, pyogrio

See [Pipfile](Pipfile) for the complete dependency list.

## Repository Map

```
trim-builder/
├── README.md                       # This file
├── Pipfile                         # Python 3.11 project manifest
├── requirements.txt                # Pinned dependencies
├── Scripts/
│   ├── webapp.py                   # Main local Flask app entrypoint
│   ├── dev.py                      # Dev convenience wrapper (auto-reload)
│   ├── trim_frontend/              # Flask application code
│   ├── trim_db/                    # Database models and ORM
│   ├── trim_core/                  # Transport model code
│   ├── mirc_core/                  # Risk model code
│   ├── trim_scripts/               # Command-line utilities and scripts
│   └── import_config/              # Pre-built import configurations
├── docker/
│   ├── Dockerfile                   # Model-Run container (QGIS-based)
│   ├── requirements.txt             # Model-Run dependencies
│   ├── prepare_dockerized_pytrim.py # Build script
│   └── getflow/
│       ├── Dockerfile_getflow      # GetFlow container (QGIS 4.2)
│       ├── requirements.txt        # GetFlow dependencies
│       └── prepare_dockerized.py   # GetFlow build script
├── iac/                            # Infrastructure as Code (AWS)
│   ├── README.md                   # Deployment & AWS setup guide
│   ├── dev.json                    # Dev environment config (example)
│   ├── requirements.txt            # Deployment tool dependencies
│   └── src/
│       ├── deployer/               # AWS deployment driver
│       └── cloudformation/         # CloudFormation templates
├── Input_Files/                    # Sample input data
└── Documentation/                  # Project documentation & notes
```

## Local Development

### 1. Environment Setup

Clone the repository and create a Python virtual environment:

```bash
git clone <repo_url> trim-builder
cd trim-builder
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 2. Database Configuration

The app uses an environment-driven DB URI resolution strategy (see engine.py):

**Option A: SQLite (default, no setup required)**
- If no environment variables are set, the app defaults to a local SQLite database.
- Used only for initial development and testing.

**Option B: PostgreSQL or MySQL (local or remote)**

Create a .env file in the Scripts directory with the following variables:

```bash
# Database connection (pick one format)

## Format 1: Direct URI
SQLALCHEMY_DATABASE_URI="postgresql+psycopg://pytrim_user:redacted_password@localhost:5432/trimdb"

## Format 2: Component-based (credentials from file or AWS Secrets Manager)
DB_ENGINE=postgres
DB_HOSTNAME=localhost
DB_PORT=5432
DB_NAME=trimdb
DB_USERNAME=pytrim_user
DB_PASSWORD=redacted_password
# (If DB_PASSWORD is omitted, the app attempts to fetch credentials from AWS Secrets Manager)

# Application configuration
FLASK_DEBUG=true
TRIM_ENV_PROFILE=local

# Mail configuration (optional, for password resets and confirmations)
MAIL_USERNAME=your-email@example.com
MAIL_DEFAULT_SENDER=your-email@example.com
MAIL_RESPONSE_ADDRESS=support@example.com

# Security configuration (dev defaults are insecure; use strong values in production)
SECRET_KEY=your-secret-key-here
SECURITY_PASSWORD_SALT=your-salt-here

# AWS profile (optional, for local development with AWS services)
LOCAL_AWS_PROFILE=your-aws-profile-name

# Login.gov integration (optional, for production environments)
LOGIN_GOV_CLIENT_ID=your-client-id
LOGIN_GOV_SECRET_ARN=arn:aws:secretsmanager:us-east-1:123456789012:secret:pytrim/login_gov/secret
LOGIN_GOV_SERVER_URL=https://wamssostg.epa.gov/oauth2/rest
# (or Login.gov prod URL)
```

**Example: Local PostgreSQL Setup**
```bash
# Install PostgreSQL (if not already installed)
# Create a database and user:
createdb trimdb
createuser -P pytrim_user  # Prompts for password

# Set environment variables
export DB_ENGINE=postgres
export DB_HOSTNAME=localhost
export DB_PORT=5432
export DB_NAME=trimdb
export DB_USERNAME=pytrim_user
export DB_PASSWORD=your_password_here
export TRIM_ENV_PROFILE=local
export FLASK_DEBUG=true
```

### 3. Database Initialization

If using a fresh database, initialize the schema:

```bash
cd Scripts
python -c "from trim_db.migrate import run_migration; run_migration('./trim_db/migrations/scripts/migrate.sql')"
```

### 4. Start the Web Application

**Option A: Dev wrapper (recommended: auto-reload on code changes)**
```bash
cd Scripts
python dev.py
# Runs on port 6060, restarts automatically when webapp.py is modified
```

**Option B: Direct entrypoint**
```bash
cd Scripts
python webapp.py -p 6060
# App is now at http://localhost:6060
# Use --expose to bind to 0.0.0.0 for external access
python webapp.py -p 6060 --expose
```

### Environment-Specific Behavior

- **TRIM_ENV_PROFILE=local**: Model execution runs locally in your Python environment (for development/testing).
- **TRIM_ENV_PROFILE=cloud**: Model execution is delegated to AWS Step Functions and ECS containers (production).
- **FLASK_DEBUG=true**: Enables hot-reload and detailed error pages (dev only).

## Docker

### Model-Run Container

The Model-Run Docker image handles the main TRIM simulation logic. It is based on QGIS to leverage geospatial capabilities.

**Build the image:**

```bash
cd docker
python prepare_dockerized_pytrim.py
docker build -t trim-model-run:latest --platform linux/amd64 .
```

See Dockerfile for the full build configuration. The image requires:
- QGIS base image
- Python 3.11 virtual environment
- Dependencies from requirements.txt

**Runtime environment variables:**
```bash
STORAGE_BUCKET_NAME=mytrim-model-run-storage-bucket
DB_ENGINE=postgres
DB_HOSTNAME=db.example.com
DB_PORT=5432
DB_NAME=trimdb
DB_USERNAME=pytrim_user
DB_PASSWORD=redacted_password
```

### GetFlow Container

The GetFlow image performs geospatial flow calculations, also based on QGIS 4.2.

**Build the image:**

```bash
cd docker/getflow
python prepare_dockerized.py
docker build -t trim-getflow:latest --platform linux/amd64 -f Dockerfile_getflow .
```

See Dockerfile_getflow for the full build configuration. The image includes:
- QGIS 4.2 base image
- Python 3.11 virtual environment with SAGA GIS support
- Dependencies from requirements.txt

**Runtime environment variables:**
Same as model-run container; output goes to a different S3 bucket:
```bash
STORAGE_BUCKET_NAME=mytrim-getflow-storage-bucket
```

### Running Containers Locally

Docker containers are normally run as ECS Fargate tasks in AWS, but you can run them locally for testing:

```bash
docker run --rm \
  -e DB_ENGINE=postgres \
  -e DB_HOSTNAME=host.docker.internal \
  -e DB_PORT=5432 \
  -e DB_NAME=trimdb \
  -e DB_USERNAME=pytrim_user \
  -e DB_PASSWORD=redacted_password \
  -e TRIM_SCENARIO_ID=12345 \
  trim-model-run:latest
```

## AWS Deployment & Infrastructure

The iac directory contains all AWS deployment automation.

**High-level overview:**
- **CloudFormation**: Provisions VPC, subnets, security groups, RDS database, S3 buckets, ECR repositories, ECS clusters, Step Functions state machines, and Elastic Beanstalk.
- **Docker**: Model-Run and GetFlow containers are built and pushed to ECR.
- **Step Functions**: Used to trigger ECS Fargate tasks to run models and retrieve results.
- **Web Tier**: Elastic Beanstalk hosts the Flask application.

To deploy or manage AWS infrastructure, see the iac/README.md.
