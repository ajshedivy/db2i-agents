# IBM i Db2 Agents - AgentOS

Welcome to IBM i Db2 Agents powered by AgentOS: a robust, production-ready application for serving IBM i-focused Agentic Applications. It includes:

- An **AgentOS instance**: An API-based interface for production-ready Agentic Applications.
- A **PostgreSQL database** for storing Agent sessions, knowledge, and memories.
- A set of **pre-built IBM i Agents** specialized for IBM i system management and monitoring.

## Available IBM i Agents

### Performance Monitoring
- **Metrics Assistant**: Analyze IBM i system performance metrics, memory pools, CPU usage, and identify bottlenecks

### Services Management
- **PTF Assistant**: Check PTF currency, identify missing PTFs, and manage system updates
- **Storage Assistant**: Analyze IFS storage usage, find large files, and identify cleanup opportunities

### Security Analysis
- **Security Assistant**: Identify exposed user profiles and generate corrective actions for security vulnerabilities

### Sample Agents
- **Employee Info**: Query employee information from the SAMPLE database (demo)

## Quick Reference

### Available Agents

| Agent ID | Name | Category | Description | CLI Command |
|----------|------|----------|-------------|-------------|
| `web-search` | Web Search Agent | Demo | Search the web using DuckDuckGo | `python cli.py --agent web-search` |
| `agno-assist` | Agno Assist | Demo | Agno framework documentation assistant | `python cli.py --agent agno-assist` |
| `metrics` | Performance Metrics Assistant | Performance | IBM i performance metrics and monitoring | `python cli.py --agent metrics` |
| `ptf` | PTF Assistant | Services | PTF (Program Temporary Fix) management | `python cli.py --agent ptf` |
| `storage` | Storage Assistant | Services | IFS storage analysis and optimization | `python cli.py --agent storage` |
| `security` | Security Assistant | Security | Security vulnerability assessment | `python cli.py --agent security` |
| `employee-info` | Employee Info Agent | Sample | Sample database queries | `python cli.py --agent employee-info` |

### Available Teams

| Team ID | Name | Type | Description | CLI Command |
|---------|------|------|-------------|-------------|
| `ptf-team` | PTF Specialist Team | Routing | Routes PTF-related queries to specialists | `python cli.py --team ptf-team` |
| `performance-routing` | Performance Routing Team | Routing | Routes performance questions to appropriate agents | `python cli.py --team performance-routing` |
| `performance-coordination` | Performance Coordination Team | Coordination | Coordinated analysis across multiple agents | `python cli.py --team performance-coordination` |
| `performance-collaboration` | Performance Collaboration Team | Collaboration | Full collaboration for comprehensive analysis | `python cli.py --team performance-collaboration` |

### Available Workflows

| Workflow ID | Name | Steps | Description | CLI Command |
|-------------|------|-------|-------------|-------------|
| `quick-performance` | Quick Performance Check | 2 steps | Fast performance overview with key metrics | `python cli.py --workflow quick-performance --prompt "Check system"` |
| `comprehensive-analysis` | Comprehensive Analysis | 4 steps | Full performance analysis with quality checks | `python cli.py --workflow comprehensive-analysis --prompt "Analyze performance"` |
| `iterative-analysis` | Iterative Analysis | Loop-based | Iterative performance analysis with refinement | `python cli.py --workflow iterative-analysis --prompt "Find bottlenecks"` |

For more information about Agno framework, checkout [Agno](https://agno.link/gh) and give it a ⭐️

## Quickstart

Follow these steps to get your Agent OS up and running:

> [Get Docker Desktop](https://www.docker.com/products/docker-desktop) should be installed and running.
> [Get OpenAI API key](https://platform.openai.com/api-keys)

### Clone the repo

```sh
git clone https://github.com/ajshedivy/db2i-agents.git
cd db2i-agents/examples/agents-infra
```

### Install dependencies

```bash
./scripts/dev_setup.sh  # Install dependencies
source .venv/bin/activate  # Activate virtual environment
```

> **Note**: Install uv if you don't have it already. See the [Development Setup](#development-setup) section for instructions.

### Configure API keys and IBM i connection

Copy the `env.example` file to `.env` and configure your credentials:

```sh
cp env.example .env
```

Then edit `.env` and set your credentials:

```sh
# OpenAI API Key (required for GPT models)
OPENAI_API_KEY="YOUR_API_KEY_HERE"

# IBM i Database Connection Credentials
HOST=your_ibm_i_hostname
DB_USER=your_db_username
PASSWORD=your_db_password
DB_PORT=8076
```
> **Note**: Use the IBM i credentials from the `.env` file from [Getting Started guide](../README.md#-getting-started)

### Supported Model Providers

This application supports multiple model providers. Make sure to set the appropriate API keys in the `.env` file for the models you intend to use:
- **OpenAI**: `OPENAI_API_KEY`
- **IBM watsonx**: `IBM_WATSONX_API_KEY`, `IBM_WATSONX_BASE_URL`, `IBM_WATSONX_MODEL_ID`, `IBM_WATSONX_PROJECT_ID`
- **Anthropic**: `ANTHROPIC_API_KEY`


### Start the application

```sh
ag infra up
```

Or run the application using docker compose (Remove the `--build` flag if you already have the image built):

```sh
docker compose up -d --build
```

This command starts:

- The **AgentOS instance**, which is a FastAPI server, running on [http://localhost:8000](http://localhost:8000).
- The **PostgreSQL database**, accessible on `localhost:5432`.

Once started, you can:

- Test the API at [http://localhost:8000/docs](http://localhost:8000/docs).

### Connect to AgentOS UI

- Open the [Agno AgentOS UI](https://os.agno.com).
- Connect your OS with `http://localhost:8000` as the endpoint. You can name it `AgentOS` (or any name you prefer).
- Explore all the features of AgentOS or go straight to the Chat page to interact with your Agents.

### Stop the application

When you're done, stop the application using:

```sh
ag infra down
```

Or:

```sh
docker compose down
```

## Using the CLI

You can also run agents, teams, and workflows directly from the command line using `cli.py`.

follow the instructions in the [CLI README](./CLI_README.md) for detailed usage examples.


## Development Setup

To setup your local virtual environment:

### Install `uv`

We use `uv` for python environment and package management. Install it by following the the [`uv` documentation](https://docs.astral.sh/uv/#getting-started) or use the command below for unix-like systems:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create Virtual Environment & Install Dependencies

Run the `dev_setup.sh` script. This will create a virtual environment and install project dependencies:

```sh
./scripts/dev_setup.sh
```

### Activate Virtual Environment

Activate the created virtual environment:

```sh
source .venv/bin/activate
```

(On Windows, the command might differ, e.g., `.venv\Scripts\activate`)

## Managing Python Dependencies

If you need to add or update python dependencies:

### Modify pyproject.toml

Add or update your desired Python package dependencies in the `[dependencies]` section of the `pyproject.toml` file.

### Generate requirements.txt

The `requirements.txt` file is used to build the application image. After modifying `pyproject.toml`, regenerate `requirements.txt` using:

```sh
./scripts/generate_requirements.sh
```

To upgrade all existing dependencies to their latest compatible versions, run:

```sh
./scripts/generate_requirements.sh upgrade
```

### Rebuild Docker Images

Rebuild your Docker images to include the updated dependencies:

```sh
docker compose up -d --build
```

## Running Tests

This project comes with a set of integration tests that you can use to ensure the application is working as expected.

First, start the application:

```sh
docker compose up -d
```

Then, run the tests:

```sh
pytest tests/
```

Then close the application again:

```sh
docker compose down
```

## Community & Support

Need help, have a question, or want to connect with the community?

- 📚 **[Read the Agno Docs](https://docs.agno.com)** for more in-depth information.
- 💬 **Chat with us on [Discord](https://agno.link/discord)** for live discussions.
- ❓ **Ask a question on [Discourse](https://agno.link/community)** for community support.
- 🐛 **[Report an Issue](https://github.com/agno-agi/agent-api/issues)** on GitHub if you find a bug or have a feature request.

## Running in Production

This repository includes a `Dockerfile` for building a production-ready container image of the application.

The general process to run in production is:

1. Update the `scripts/build_image.sh` file and set your IMAGE_NAME and IMAGE_TAG variables.
2. Build and push the image to your container registry:

```sh
./scripts/build_image.sh
```

3. Run in your cloud provider of choice.

### Detailed Steps

1. **Configure for Production**

- Ensure your production environment variables (e.g., `OPENAI_API_KEY`, database connection strings) are securely managed. Most cloud providers offer a way to set these as environment variables for your deployed service.
- Review the agent configurations in the `/agents` directory and ensure they are set up for your production needs (e.g., correct model versions, any production-specific settings).

2. **Build Your Production Docker Image**

- Update the `scripts/build_image.sh` script to set your desired `IMAGE_NAME` and `IMAGE_TAG` (e.g., `your-repo/agent-api:v1.0.0`).
- Run the script to build and push the image:

  ```sh
  ./scripts/build_image.sh
  ```

3. **Deploy to a Cloud Service**
   With your image in a registry, you can deploy it to various cloud services that support containerized applications. Some common options include:

- **Serverless Container Platforms**:

  - **Google Cloud Run**: A fully managed platform that automatically scales your stateless containers. Ideal for HTTP-driven applications.
  - **AWS App Runner**: Similar to Cloud Run, AWS App Runner makes it easy to deploy containerized web applications and APIs at scale.
  - **Azure Container Apps**: Build and deploy modern apps and microservices using serverless containers.

- **Container Orchestration Services**:

  - **Amazon Elastic Container Service (ECS)**: A highly scalable, high-performance container orchestration service that supports Docker containers. Often used with AWS Fargate for serverless compute or EC2 instances for more control.
  - **Google Kubernetes Engine (GKE)**: A managed Kubernetes service for deploying, managing, and scaling containerized applications using Google infrastructure.
  - **Azure Kubernetes Service (AKS)**: A managed Kubernetes service for deploying and managing containerized applications in Azure.

- **Platform as a Service (PaaS) with Docker Support**

  - **Railway.app**: Offers a simple way to deploy applications from a Dockerfile. It handles infrastructure, scaling, and networking.
  - **Render**: Another platform that simplifies deploying Docker containers, databases, and static sites.
  - **Heroku**: While traditionally known for buildpacks, Heroku also supports deploying Docker containers.

- **Specialized Platforms**:
  - **Modal**: A platform designed for running Python code (including web servers like FastAPI) in the cloud, often with a focus on batch jobs, scheduled functions, and model inference, but can also serve web endpoints.

The specific deployment steps will vary depending on the chosen provider. Generally, you'll point the service to your container image in the registry and configure aspects like port mapping (the application runs on port 8000 by default inside the container), environment variables, scaling parameters, and any necessary database connections.

4. **Database Configuration**

- The default `docker-compose.yml` sets up a PostgreSQL database for local development. In production, you will typically use a managed database service provided by your cloud provider (e.g., AWS RDS, Google Cloud SQL, Azure Database for PostgreSQL) for better reliability, scalability, and manageability.
- Ensure your deployed application is configured with the correct database connection URL for your production database instance. This is usually set via an environment variables.
