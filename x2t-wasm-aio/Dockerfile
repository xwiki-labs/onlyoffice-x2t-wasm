# This Dockerfile takes most of its commands from
# https://helpcenter.onlyoffice.com/server/linux/document/compile-source-code.aspx,
# which hallows to build the complete OnlyOffice Document Server
# We tweak it a bit so that we build only the tool that we are looking for (x2t) 
from ubuntu:trusty as onlyoffice-build

run apt-get update
run apt-get install --force-yes -yq \
    wget \
    build-essential \
    libcurl4-gnutls-dev \
    libglib2.0-dev \
    libgdk-pixbuf2.0-dev \
    libgtkglext1-dev \
    libatk1.0-dev \
    libcairo2-dev \
    libxml2-dev \
    libxss-dev \
    libgconf2-dev \
    default-jre \
    qt5-qmake \
    qt5-default  \
    p7zip-full \
    git \
    subversion

run git clone https://github.com/ONLYOFFICE/core.git

# Build the 3rd party dependencies
run cd core/Common/3dParty && ./make.sh

# Add a target for the build only for x2t and its dependencies
run echo "x2t: \$(X2T)" >> core/Makefile
# Check the file contents
run tail core/Makefile

run cd core && make x2t

# We now have a working build of x2t for amd64 ; let's port it to WebAssembly
from ubuntu:bionic

run apt-get update && apt-get install --force-yes -yq build-essential git

copy --from=onlyoffice-build /core /core

run apt-get install -y python cmake

# Download the Emscripten sdk
run git clone https://github.com/emscripten-core/emsdk.git
run cd emsdk && ./emsdk install latest
#run cd emsdk && ./emsdk install sdk-upstream-incoming-64bit
run cd emsdk && ./emsdk activate latest
#run cd emsdk && ./emsdk activate sdk-upstream-incoming-64bit
run find /core/X2tConverter -name "Makefile"

run apt-get install -y qt5-qmake

run /bin/bash -c "source ./emsdk/emsdk_env.sh && cd /core/X2tConverter/build/Qt/X2tSLN.build && make clean && /emsdk/upstream/emscripten/emmake make"
# && mkdir final-build && cd final-build && emcc /core/X2tConverter/build/Qt/core_build/linux_64/release/obj/main.o"
# ../emsdk/upstream/emscripten/emmake make x2t"
# At this point, check if 
# * 3rdParty should be ported (probably)
