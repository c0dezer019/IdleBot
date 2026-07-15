# syntax=docker/dockerfile:1
ARG REDIS_VERSION=7.4-alpine

FROM redis:${REDIS_VERSION}

RUN mkdir -p /var/lib/redis

COPY --chown=redis:redis redis.conf /usr/local/etc/redis/redis.conf

VOLUME ["/var/lib/redis"]

EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD redis-cli -h 127.0.0.1 -p 6379 ping | grep -q PONG || exit 1

# Named volume mounts as root-owned each fresh volume; fix perms then run as root (dev only).
ENTRYPOINT ["sh", "-c", "chown -R redis:redis /var/lib/redis && exec redis-server /usr/local/etc/redis/redis.conf"]
