FROM kbase/rtmin:1.2
WORKDIR /kb
RUN git clone https://github.com/kbase/dev_container
WORKDIR /kb/dev_container/modules
RUN git clone https://github.com/kbase/jars
RUN git clone https://github.com/kbase/auth
RUN git clone https://github.com/kbase/kbapi_common
WORKDIR /kb/dev_container
RUN ./bootstrap /kb/runtime/
ENV KB_TOP /kb/dev_container
ENV KB_RUNTIME /kb/runtime/
ENV TARGET $KB_TOP
ENV DEPLOY_RUNTIME=$KB_RUNTIME
RUN make
RUN mkdir -p /kb/deployment
RUN mkdir -p /kb/deployment/bin
RUN mkdir -p /kb/deployment/lib
RUN mkdir -p /kb/deployment/services
ENV TARGET /kb/deployment
WORKDIR /kb/dev_container/modules/jars
RUN make deploy
WORKDIR /kb/dev_container/modules/auth
RUN make deploy
WORKDIR /kb/dev_container/modules/kbapi_common
RUN make deploy
######################### end of kbase/devmin:1.1
RUN apt-get update && apt-get install -y \
build-essential \
python-dev \
python-setuptools \
python-numpy \
python-scipy \
libatlas-dev \
libatlas3gf-base
RUN pip install scikit-learn
RUN pip install scipy
RUN apt-get install -y mongodb
WORKDIR /kb/dev_container/modules
######################### AWE binaries
RUN git clone https://github.com/kbase/awe_service
WORKDIR /kb/dev_container/modules/awe_service
RUN mkdir bin
RUN mkdir gopath
ENV GOPATH /kb/dev_container/modules/awe_service/gopath
RUN mkdir -p $GOPATH/src/github.com/MG-RAST
RUN git submodule init
RUN git submodule update
RUN cp -r AWE $GOPATH/src/github.com/MG-RAST/
RUN mkdir -p $GOPATH/src/github.com/docker
RUN wget -O $GOPATH/src/github.com/docker/docker.zip https://github.com/docker/docker/archive/v1.6.1.zip
RUN unzip -d $GOPATH/src/github.com/docker $GOPATH/src/github.com/docker/docker.zip
RUN mv -v $GOPATH/src/github.com/docker/docker-1.6.1 $GOPATH/src/github.com/docker/docker
RUN go get -v github.com/MG-RAST/AWE/...
RUN cp $GOPATH/bin/awe-server /kb/runtime/bin/
RUN cp $GOPATH/bin/awe-client /kb/runtime/bin/
