FROM modelcpp/codecompass:runtime-pgsql

RUN DEBIAN_FRONTEND=noninteractive apt-get update                              \ 
&&  DEBIAN_FRONTEND=noninteractive apt-get install --yes zip

COPY bin/start_parse.sh /tmp
RUN chmod a+x /tmp/start_parse.sh

WORKDIR /tmp
CMD ["/tmp/start_parse.sh","/tmp/project_source.zip"]
