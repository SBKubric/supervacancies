FROM amazon/aws-cli:2.11.14

COPY ./compose/production/aws/maintenance /usr/local/bin/maintenance
COPY ./compose/production/postgres/maintenance/* /usr/local/bin/maintenance/
COPY ./compose/production/postgres/maintenance/_sourced /usr/local/bin/maintenance/_sourced

RUN chmod +x /usr/local/bin/maintenance/* && mv /usr/local/bin/maintenance/* /usr/bin/ \
    && rmdir /usr/local/bin/maintenance && install_repos && rm /usr/bin/install_repos && yum update -y && yum install -y postgresql14 && yum install -y postgresql14-libs && yum install -y gzip && yum clean all

ENTRYPOINT ["/bin/sh"]
