FROM fedora:31
USER root
RUN yum install -y git python3-cherrypy
RUN git clone https://github.com/cloud-bulldozer/bohica
RUN mkdir -p /opt/bohica/
COPY . /opt/bohica/
