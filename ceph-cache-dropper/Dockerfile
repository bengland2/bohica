FROM rook/ceph:master

USER root
RUN yum install -y git python-cherrypy
RUN mkdir -p /opt/ceph_cache_drop
# assumes you are doing sudo podman build -f Dockerfile .
COPY . /opt/ceph_cache_drop
WORKDIR /opt/ceph_cache_drop
ENTRYPOINT python osd-cache-drop-websvc.py
