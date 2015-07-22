import memcache


class MemcacheClient():
    """
    memcache wrapper
    """
    hostname = ''
    client = ''
    prefix = ''
    time = 0

    def __init__(self, hostname="127.0.0.1", port=11211, prefix='poseidon', time=900):
        # TODO: set the memcache settings in the config
        self.hostname = "%s:%s" % (hostname, port)
        self.client = memcache.Client([self.hostname])
        self.prefix = prefix
        self.time = time

    def _prefix_key(self, key):
        """
        manually handle prefixing the keys
        """
        if self.prefix:
            prefix_key = '%s:%s' % (self.prefix, key)
        else:
            prefix_key = key

        return str(prefix_key)

    def cas(self, key, val, min_compress_len=0):
        """
        Sets a key to a given value in the memcache if it hasn't been
        altered since last fetched. (See L{gets}).

        The C{key} can optionally be an tuple, with the first element
        being the server hash value and the second being the key.
        If you want to avoid making this module calculate a hash value.
        You may prefer, for example, to keep all of a given user's objects
        on the same memcache server, so you could use the user's unique
        id as the hash value.

        @return: Nonzero on success.
        @rtype: int
        @param time: Tells memcached the time which this value should expire,
        either as a delta number of seconds, or an absolute unix
        time-since-the-epoch value. See the memcached protocol docs section
        "Storage Commands" for more info on <exptime>. We default to
        0 == cache forever.
        @param min_compress_len: The threshold length to kick in
        auto-compression of the value using the zlib.compress() routine. If
        the value being cached is a string, then the length of the string is
        measured, else if the value is an object, then the length of the
        pickle result is measured. If the resulting attempt at compression
        yeilds a larger string than the input, then it is discarded. For
        backwards compatability, this parameter defaults to 0, indicating
        don't ever try to compress.
        """
        prefixed_key = self._prefix_key(key)
        return self.client.cas(prefixed_key, val, self.time, min_compress_len)

    def reset_cas(self):
        """
        Reset the cas cache.  This is only used if the Client() object
        was created with "cache_cas=True".  If used, this cache does not
        expire internally, so it can grow unbounded if you do not clear it
        yourself.
        """
        self.client.reset_cas()

    def set_servers(self, servers):
        """
        Set the pool of servers used by this client.

        @param servers: an array of servers.
        Servers can be passed in two forms:
            1. Strings of the form C{"host:port"}, which implies a default weight of 1.
            2. Tuples of the form C{("host:port", weight)}, where C{weight} is
            an integer weight value.
        """
        self.client.set_servers(servers)

    def get_stats(self):
        return self.client.get_stats()

    def get_slabs(self):
        return self.client.get_slabs()

    def debuglog(self, message):
        self.client.debuglog(message)

    def forget_dead_hosts(self):
        self.client.forget_dead_hosts()

    def disconnect_all(self):
        self.client.disconnect_all()

    def flush_all(self):
        """
        Expire all data in memcache servers that are reachable.
        """
        self.client.flush_all()

    def add(self, key, value, min_compress_len=0):
        """
        Add new key with value.

        Like L{set}, but only stores in memcache if the key doesn't already exist.

        @return: Nonzero on success.
        @rtype: int
        """
        prefixed_key = self._prefix_key(key)
        return self.client.add(prefixed_key, value, time=self.time, min_compress_len=min_compress_len)

    def append(self, key, value, min_compress_len=0):
        """
        Append the value to the end of the existing key's value.

        Only stores in memcache if key already exists.
        Also see L{prepend}.

        @return: Nonzero on success.
        @rtype: int
        """
        prefixed_key = self._prefix_key(key)
        return self.client.append(prefixed_key, value, time=self.time, min_compress_len=min_compress_len)

    def prepend(self, key, value, min_compress_len=0):
        """
        Prepend the value to the beginning of the existing key's value.

        Only stores in memcache if key already exists.
        Also see L{append}.

        @return: Nonzero on success.
        @rtype: int
        """
        prefixed_key = self._prefix_key(key)
        return self.client.prepend(prefixed_key, value, time=self.time, min_compress_len=min_compress_len)

    def replace(self, key, value, min_compress_len=0):
        """
        Replace existing key with value.

        Like L{set}, but only stores in memcache if the key already exists.
        The opposite of L{add}.

        @return: Nonzero on success.
        @rtype: int
        """
        prefixed_key = self._prefix_key(self)
        return self.client.replace(prefixed_key, valur, time=self.time, min_compress_len=min_compress_len)

    def incr(self, key, delta=1):
        """
        increment the value of the key
        """
        prefixed_key = self._prefix_key(key)
        return self.client.incr(prefixed_key, delta=delta)

    def decr(self, key, delta=1):
        """
        decrement the value of the key
        """
        prefixed_key = self._prefix_key(key)
        return self.client.decr(prefixed_key, delta=1)

    def set(self, key, value):
        """
        add a new value to the cache
        """
        from poseidon import logger
        prefixed_key = self._prefix_key(key)
        logger.debug('set memcache key %s' % prefixed_key)
        return self.client.set(prefixed_key, value, time=self.time)

    def get(self, key):
        """
        get a value from a key
        """
        from poseidon import logger
        prefixed_key = self._prefix_key(key)
        logger.debug('get memcache key %s' % prefixed_key)
        return self.client.get(prefixed_key)

    def gets(self, key):
        """
        Retrieves a key from the memcache. Used in conjunction with 'cas'.

        @return: The value or None.
        """
        prefixed_key = self._prefix_key(key)
        return self.client.gets(prefixed_key)

    def delete(self, key):
        """
        remove the key from the cache
        """
        from poseidon import logger
        prefixed_key = self._prefix_key(key)
        logger.debug('delete memcache key %s' % prefixed_key)
        return self.client.delete(prefix_key)

    def get_multi(self, keys):
        """
        get multiple keys
        """
        prefixed_keys = [self._prefix_key(key) for key in keys]
        return self.client.get_multi(prefixed_keys)

    def set_multi(self, elements):
        """
        set multiple keys
        """
        prefixed_elements = {}

        for key, value in elements.items():
            prefixed_elements[self._prefix_key(key)] = value

        return self.client.set_multi(prefixed_elements, time=self.time)

    def delete_multi(self, keys):
        """
        delete multiple keys
        """
        prefixed_keys = [self._prefix_key(key) for key in keys]
        return self.client.delete_multi(prefixed_keys)

    def check_key(self, key, key_extra_len=0):
        prefixed_key = self._prefix_key(key)
        return self.check_key(prefix_key, key_extra_len=key_extra_len)
