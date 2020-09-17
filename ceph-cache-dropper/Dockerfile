FROM fedora:31

RUN dnf install -y --nodocs python3 python3-cherrypy wget
RUN ln -s /usr/bin/python3 /usr/bin/python
COPY . /opt/ceph_cache_drop
WORKDIR /opt/ceph_cache_drop
RUN wget https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/linux/amd64/kubectl
RUN chmod +x /opt/ceph_cache_drop/kubectl
ENTRYPOINT python3 osd-cache-drop-websvc.py
