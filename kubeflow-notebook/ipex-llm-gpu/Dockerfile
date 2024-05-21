
ARG BASE_IMG=docker.io/kubeflownotebookswg/jupyter
FROM $BASE_IMG

# common environemnt variables
ENV NB_USER jovyan
ENV NB_UID 1000

# install - conda packages
# NOTE: we use mamba to speed things up
RUN mamba install -y -q \
    bokeh==3.2.2 \
    cloudpickle==2.2.1 \
    dill==0.3.7 \
    ipympl==0.9.3 \
    matplotlib==3.8.0 \
    pandas==2.1.1 \
    scikit-image==0.22.0 \
    scikit-learn==1.3.1 \
    scipy==1.11.3 \
    seaborn==0.13.0 \
 && mamba clean -a -f -y

# install - requirements.txt
COPY --chown=${NB_USER}:users requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt --quiet --no-cache-dir \
 && rm -f /tmp/requirements.txt

 # switch to root for create directory
 USER root
 RUN mkdir -p ipex-llm && \
    cd ./ipex-llm


# Configure ipex-llm for GPU
RUN curl -fsSL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2023.PUB | gpg --dearmor | tee /usr/share/keyrings/intel-oneapi-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/intel-oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main " > /etc/apt/sources.list.d/oneAPI.list && \
    apt-get update && \
    apt-get install -y curl wget git gnupg gpg-agent && \
    wget -qO - https://repositories.intel.com/graphics/intel-graphics.key | gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg && \
    echo 'deb [arch=amd64,i386 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu jammy arc' | tee /etc/apt/sources.list.d/intel.gpu.jammy.list && \
    pip install --pre --upgrade ipex-llm[xpu] --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/ && \
    # Fix Trivy CVE Issues
    python3 -m pip install transformers==4.36.2 && \
    python3 -m pip install transformers_stream_generator einops tiktoken && \
    # Install opencl-related repos
    apt-get update && \
    apt-get install -y intel-opencl-icd intel-level-zero-gpu=1.3.26241.33-647~22.04 level-zero level-zero-dev --allow-downgrades && \
    # Install oneAPI
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list && \
    apt update && \
    apt-get install -y intel-oneapi-common-vars=2024.0.0-49406 intel-oneapi-common-oneapi-vars=2024.0.0-49406 intel-oneapi-diagnostics-utility=2024.0.0-49093 \
    intel-oneapi-compiler-dpcpp-cpp=2024.0.2-49895 intel-oneapi-dpcpp-ct=2024.0.0-49381 \
    intel-oneapi-mkl=2024.0.0-49656 intel-oneapi-mkl-devel=2024.0.0-49656 \
    intel-oneapi-mpi=2021.11.0-49493 intel-oneapi-mpi-devel=2021.11.0-49493 \
    intel-oneapi-dal=2024.0.1-25 intel-oneapi-dal-devel=2024.0.1-25 \
    intel-oneapi-ippcp=2021.9.1-5 intel-oneapi-ippcp-devel=2021.9.1-5 intel-oneapi-ipp=2021.10.1-13 intel-oneapi-ipp-devel=2021.10.1-13 \
    intel-oneapi-tlt=2024.0.0-352 intel-oneapi-ccl=2021.11.2-5 intel-oneapi-ccl-devel=2021.11.2-5 \
    intel-oneapi-dnnl-devel=2024.0.0-49521 intel-oneapi-dnnl=2024.0.0-49521 \
    intel-oneapi-tcm-1.0=1.0.0-435 && \
    python3 -m pip install --upgrade colorama && \
    # Install vllm dependencies
    python3 -m pip install --upgrade fastapi && \
    python3 -m pip install --upgrade "uvicorn[standard]" && \
    # Download vLLM-Serving
    git clone https://github.com/intel-analytics/IPEX-LLM && \
    cp -r ./IPEX-LLM/python/llm/example/GPU/vLLM-Serving/ ./vLLM-Serving && \
    rm -rf ./IPEX-LLM 

# switch to NB_UID for installs
USER $NB_UID