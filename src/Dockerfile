FROM python:3.12-slim-bookworm AS build

COPY ./requirements.txt requirements.txt

ARG clang_upstream_version=18
ARG clang_debian_version=16

RUN export distro=$(cat /etc/os-release | grep VERSION_CODENAME= | cut -d= -f2) && \
    export arch=$(dpkg --print-architecture) && \
    apt -y update && \
    apt -y install --no-install-recommends catatonit curl gpg && \
    curl -fsSL https://apt.llvm.org/llvm-snapshot.gpg.key | gpg --dearmor -o /etc/apt/keyrings/llvm-snapshot.gpg && \
    echo "deb [arch=\"${arch}\" signed-by=/etc/apt/keyrings/llvm-snapshot.gpg] http://apt.llvm.org/${distro} llvm-toolchain-${distro}-${clang_upstream_version} main\ndeb-src [arch=\"${arch}\" signed-by=/etc/apt/keyrings/llvm-snapshot.gpg] http://apt.llvm.org/${distro} llvm-toolchain-${distro}-${clang_upstream_version} main" >> /etc/apt/sources.list.d/llvm.list && \
    apt -y update && \
    bash -c 'if [[ "${arch}" == @(amd64|arm64|i386|s360x) ]] ; then echo "Arch clang: ${arch}" ; apt -y install --no-install-recommends gcc g++ libffi-dev patchelf clang-${clang_upstream_version} lldb-${clang_upstream_version} lld-${clang_upstream_version} ; else echo "Arch clang: ${arch}" ; apt -y install --no-install-recommends gcc g++ libffi-dev patchelf clang-${clang_debian_version} lldb-${clang_debian_version} lld-${clang_debian_version} ; fi' && \
    apt -y download zlib1g && \ 
    mkdir -p /librequirements && \
    dpkg -i --force-all --root=/librequirements zlib1g*.deb && \
    pip3 install -r requirements.txt && \
    pip3 install nuitka

WORKDIR /app
COPY ./main.py ./stats.py /app

RUN export arch=$(dpkg --print-architecture) && \
    bash -c 'if [[ "${arch}" == @(amd64|arm64|i386|s360x) ]] ; then export CXX=/usr/bin/clang++-${clang_upstream_version} ; export CC=/usr/bin/clang-${clang_upstream_version} ; else export CXX=/usr/bin/clang++-${clang_debian_version} ; export CC=/usr/bin/clang-${clang_debian_version} ; fi && export && python3 -m nuitka --show-scons --clang --follow-imports --include-plugin-directory=/app --standalone --output-filename=omni main.py'

FROM gcr.io/distroless/base-debian12:latest

COPY --from=build --chmod=0755 /usr/libexec/podman/catatonit /catatonit
COPY --from=build --chmod=0755 /librequirements /
COPY --from=build --chmod=0755 /app/main.dist /omni

ENTRYPOINT [ "/catatonit", "--" ]
CMD [ "/omni/omni"]
