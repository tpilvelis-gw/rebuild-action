FROM glasswallsolutions/evaluationsdk:1

RUN yum install -y python3
COPY hello.py /hello.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" , "-v" , $GITHUB_WORKSPACE ]