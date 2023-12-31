# You can pick any Debian/Ubuntu-based image. 😊
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Options for setup script
ARG INSTALL_ZSH="true"
ARG UPGRADE_PACKAGES="false"
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# Install needed packages and setup non-root user. Use a separate RUN statement to add your own dependencies.
COPY library-scripts/*.sh /tmp/library-scripts/
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && /bin/bash /tmp/library-scripts/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}" "true" "true" \
    && apt-get install -y pkg-config zip g++ zlib1g-dev unzip

# Installing python 3.11 and pip
RUN apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \ 
    && apt-get update \
    && apt-get install -y python3.11 python3-pip \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install Bazel
ARG BAZELISK_VERSION=v1.18.0
ARG BAZELISK_DOWNLOAD_SHA=dev-mode
RUN curl -fSsL -o /usr/local/bin/bazelisk https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-amd64 \
    && ([ "${BAZELISK_DOWNLOAD_SHA}" = "dev-mode" ] || echo "${BAZELISK_DOWNLOAD_SHA} */usr/local/bin/bazelisk" | sha256sum --check - ) \
    && chmod 0755 /usr/local/bin/bazelisk

# Install MongoDB command line tools
ARG MONGO_TOOLS_VERSION=7.0
RUN . /etc/os-release \
    && curl -fsSL "https://pgp.mongodb.com/server-${MONGO_TOOLS_VERSION}.asc" | gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg] http://repo.mongodb.org/apt/ubuntu ${VERSION_CODENAME}/mongodb-org/${MONGO_TOOLS_VERSION} multiverse" | tee /etc/apt/sources.list.d/mongodb-org-${MONGO_TOOLS_VERSION}.list \
    && apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y mongodb-mongosh \
    && if [ "$(dpkg --print-architecture)" = "amd64" ]; then apt-get install -y mongodb-database-tools; fi

# Install CUDA
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    && apt-get update \
    && apt-get -y install cuda

ENV PATH="$PATH:/usr/local/cuda/bin"
ENV CUDA_PATH="/usr/local/cuda"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64"

# Installing chrome for FE testing
RUN apt-get install -y fonts-liberation libu2f-udev libvulkan1 xdg-utils \
    && curl -fSsL -o google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# These files need to be removed, since they will be created with gpu passthrough and will fail otherwise
RUN rm -rf /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1 \
           /usr/lib/x86_64-linux-gnu/libcuda.so.1 \
           /usr/lib/x86_64-linux-gnu/libcudadebugger.so.1

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# Cleanup
RUN apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts