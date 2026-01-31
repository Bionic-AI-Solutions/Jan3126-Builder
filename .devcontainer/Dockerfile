# Use Python 3.11 base image and add Node.js
FROM python:3.11-slim-bullseye

# Install common development tools and dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    build-essential \
    curl \
    git \
    vim \
    ca-certificates \
    gnupg \
    lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x (pinned to specific version for reproducibility)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && node --version && npm --version

# Install Poetry for Python dependency management (pinned version)
RUN pip3 install --no-cache-dir "poetry>=1.7.0,<2.0.0" \
    && poetry --version

# Install kubectl (fixed command substitution)
RUN KUBECTL_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt) \
    && curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/kubectl \
    && kubectl version --client

# Install Docker CLI (will use host's Docker daemon via mounted socket)
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI (gh)
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && gh --version

# Install common Python packages (with version constraints for stability)
RUN pip3 install --no-cache-dir \
    "black>=23.0.0" \
    "flake8>=6.0.0" \
    "pylint>=3.0.0" \
    "pytest>=7.0.0" \
    "pytest-asyncio>=0.21.0" \
    "mypy>=1.0.0"

# Install common Node.js packages globally (with version constraints)
RUN npm install -g \
    "typescript@^5.0.0" \
    "ts-node@^10.9.0" \
    "eslint@^8.0.0" \
    "prettier@^3.0.0" \
    "nodemon@^3.0.0" \
    "@types/node@^20.0.0"

# Create vscode user and docker group (GID 999 matches common host docker group for socket access)
RUN groupadd --gid 1000 vscode \
    && groupadd --gid 999 docker 2>/dev/null || true \
    && useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode \
    && usermod -aG docker vscode \
    && mkdir -p /home/vscode/.local/bin \
    && chown -R vscode:vscode /home/vscode

# Set up workspace directory
WORKDIR /workspace

# Switch to vscode user
USER vscode

# Set up Python environment
ENV PATH="/home/vscode/.local/bin:${PATH}"
