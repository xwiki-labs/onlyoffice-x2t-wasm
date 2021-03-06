# This Dockerfile takes most of its commands from
# https://helpcenter.onlyoffice.com/server/linux/document/compile-source-code.aspx,
# which hallows to build the complete OnlyOffice Document Server
# We tweak it a bit so that we build only the tool that we are looking for (x2t) 
from ubuntu:xenial

# We now have a working build of x2t for amd64 ; let's port it to WebAssembly
# Install emsdk
# ------------------------------------------------------------------------------

# Supports only 1.38.40+, accpets also '-upstream' variants
ARG EMSCRIPTEN_VERSION=1.39.4
ARG EMSDK_CHANGESET=master

# ------------------------------------------------------------------------------

ENV EMSDK /emsdk
ENV EM_DATA ${EMSDK}/.data
ENV EM_CONFIG ${EMSDK}/.emscripten
ENV EM_CACHE ${EM_DATA}/cache
ENV EM_PORTS ${EM_DATA}/ports

# ------------------------------------------------------------------------------

RUN echo "## Start building" \
    \
&&	echo "## Update and install packages" \
    &&	apt-get -qq -y update \
    &&  apt-get -qq install -y --no-install-recommends \
            libxml2 \
            wget \
            git-core \
            ca-certificates \
            build-essential \
            file \
            python python-pip \
            python3 python3-pip \
            curl \
    \
&&  echo "## Done"

# Install node 13
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get install -y nodejs

RUN  echo "## Get EMSDK" \
    &&  git clone https://github.com/emscripten-core/emsdk.git ${EMSDK} \
    &&  cd ${EMSDK} && git reset --hard ${EMSDK_CHANGESET} \
    \
    &&  ./emsdk.py update-tags \
&&  echo "## Done"

RUN  echo "## Install Emscripten" \
    &&  cd ${EMSDK} \
    && ./emsdk install ${EMSCRIPTEN_VERSION} \
    \
&&  echo "## Done"

# This generates configuration that contains all valid paths according to installed SDK
RUN cd ${EMSDK} \
    &&  echo "## Generate standard configuration" \
    \
    &&  ./emsdk activate ${EMSCRIPTEN_VERSION} --embedded \
    &&  ./emsdk construct_env > /dev/null \
    &&  cat ${EMSDK}/emsdk_set_env.sh \
    \
    # remove wrongly created entry with EM_CACHE, variable will be picked up from ENV
    &&  sed -i -e "/EM_CACHE/d" ${EMSDK}/emsdk_set_env.sh \
    # add a link to tools like asm2wasm in a system path
    # asm2wasm (and friends might be places either in ./upstream of ./fastcomp folder, hence detection is needed)
    &&  printf "export PATH=$(dirname $(find . -name asm2wasm -exec readlink -f {} +)):\$PATH\n" >> ${EMSDK}/emsdk_set_env.sh \
    \
&&  echo "## Done"

# Create a structure and make mutable folders accessible for r/w
RUN cd ${EMSDK} \
    &&  echo "## Create .data structure" \
    &&  for mutable_dir in ${EM_DATA} ${EM_PORTS} ${EM_CACHE} ${EMSDK}/zips ${EMSDK}/tmp; do \
            mkdir -p ${mutable_dir}; \
            chmod -R 777 ${mutable_dir}; \
        done \
        \
&&  echo "## Done"

# Create symbolic links for critical Emscripten Tools
# This is important for letting people using Emscripten in Dockerfiles without activation
# As each Emscripten release is placed to a different folder (i.e. /emsdk/emscripten/tag-1.38.31)
RUN echo "## Create symbolic links" \
    &&  . ${EMSDK}/emsdk_set_env.sh \
    \
    &&  mkdir -p ${EMSDK}/llvm ${EMSDK}/emscripten ${EMSDK}/binaryen \
    \
    &&  ln -s $(dirname $(which node))/..       ${EMSDK}/node/current \
    &&  ln -s $(dirname $(which clang))/..      ${EMSDK}/llvm/clang \
    &&  ln -s $(dirname $(which emcc))          ${EMSDK}/emscripten/sdk \
    \
    &&  ln -s $(dirname $(which asm2wasm))      ${EMSDK}/binaryen/bin \
    \
    &&  echo "## Done"

# Clean up emscripten installation and strip some symbols
RUN echo "## Aggresive optimization: Remove debug symbols" \
&&  apt-get -qq -y update && apt-get -qq install -y --no-install-recommends \
        binutils \
    && . ${EMSDK}/emsdk_set_env.sh \
    # Remove debugging symbols from embedded node (extra 7MB)
    && strip -s `which node` \
    # Tests consume ~80MB disc space
    && rm -fr ${EMSDK}/llvm/clang/emscripten/tests \
    # strip out symbols from clang (~extra 50MB disc space)
    && find ${EMSDK}/llvm/clang/bin -type f -exec strip -s {} + || true \
    && find ${EMSDK}/llvm/clang/fastcomp/bin -type f -exec strip -s {} + || true \
&&  echo "## Done"

# Populate Emscripten SDK cache with libc++, to improve further compilation times.
RUN echo "## Pre-populate cache" \
    &&  . ${EMSDK}/emsdk_set_env.sh \
    \
    &&  embuilder.py build SYSTEM \
    \
    &&  mkdir -p /tmp/emscripten_test \
    &&  cd /tmp/emscripten_test \
    \
        &&  printf '#include <iostream>\nint main(){std::cout << "HELLO FROM DOCKER C++"<<std::endl;return 0;}' > test.cpp \
        &&  em++ --std=c++11 test.cpp -o test.js -s WASM=0 &&  node test.js \
        &&  em++ --std=c++11 -g3 test.cpp -o test.js -s WASM=0 &&  node test.js \
        &&  em++ --std=c++11 test.cpp -o test.js -s WASM=1 &&  node test.js \
    \
    &&  cd / \
    &&  rm -fr /tmp/emscripten_test \
    \
    # some files were created, and we need to make sure that those can be accessed by non-root people
    &&  chmod -R 777 ${EM_DATA} \
    \
    # cleanup
    &&  find ${EMSDK} -name "*.pyc" -exec rm {} \; \
    \
    &&  echo "## Done"

# Test emsdk
RUN . ${EMSDK}/emsdk_set_env.sh  \
    && emcc --version \
    && mkdir -p /tmp/emscripten_test && cd /tmp/emscripten_test \
    && printf '#include <iostream>\nint main(){std::cout<<"HELLO"<<std::endl;return 0;}' > test.cpp \
    && em++ -O2 test.cpp -o test.js && nodejs test.js \
    && em++ test.cpp -o test.js && nodejs test.js \
    && cd / \
    && rm -rf /tmp/emscripten_test \

