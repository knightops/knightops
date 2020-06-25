import redis


class RedisClient(object):
    def __init__(self, host, port, max_connections, auth=None, db=0):
        # 初始化redis链接
        if auth is None or auth.strip() is '':
            auth = None
        self._connection = redis.StrictRedis(connection_pool=self.create_pool(host, port, max_connections, db, auth))

    @staticmethod
    def create_pool(host, port, max_connections, db=0, auth=None):
        # 设置redis连接池
        return redis.ConnectionPool(
            max_connections=max_connections,
            host=host,
            port=port,
            db=db,
            password=auth)

    def set_data(self, key, value, ex=None, nx=False):
        return self._connection.set(key, value, ex, None, nx)

    def get_data(self, key):
        return self._connection.get(key)

    def del_data(self, key):
        return self._connection.delete(key)

    def zrange_by_score_data(self, key, min_value, max_value, offset=None, count=None):
        return self._connection.zrangebyscore(key, min_value, max_value, offset, count)

    def flush_db(self):
        self._connection.flushdb()

    def hgetall(self, name):
        hget_result = dict(self._connection.hgetall(name))
        # 处理取出的二进制数据并且转成str重新赋值
        for k in hget_result:
            if isinstance(k, bytes):
                key = bytes.decode(k)
            else:
                key = k
            v = hget_result.get(k)
            if isinstance(v, bytes):
                value = bytes.decode(v)
            else:
                value = v
            hget_result.pop(k)
            hget_result[key] = value
        return hget_result

    def hset(self, name, key, value):
        self._connection.hset(name, key, value)

    def hmset(self, key, value):
        self._connection.hmset(key, value)

    def get_connection(self):
        return self._connection

    def set_incr(self, key, amount=1):
        return self._connection.incr(key, amount)

    def set_decr(self, key, amount=1):
        return self._connection.decr(key, amount)

    def set_expire(self, key, ex=None):
        return self._connection.expire(key, ex)

    def key_exists(self, key):
        return self._connection.exists(key)

    def key_ttl(self, key):
        return self._connection.ttl(key)