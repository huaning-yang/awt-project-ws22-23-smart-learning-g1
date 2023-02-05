FROM neo4j:latest

COPY --chown=neo4j import/neo4j.dump neo4j.dump
COPY --chown=neo4j mgt-entrypoint.sh mgt-entrypoint.sh
RUN chmod +x mgt-entrypoint.sh

ENTRYPOINT ["./mgt-entrypoint.sh"]