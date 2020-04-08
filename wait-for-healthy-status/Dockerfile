FROM rook/ceph:master
USER root
RUN yum install -y git python2-cherrypy
RUN mkdir -p /opt/bohica
COPY wait-for-healthy-status/ /opt/bohica/
