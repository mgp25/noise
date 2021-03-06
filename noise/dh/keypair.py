class KeyPair(object):
    def __init__(self, public_key, private_key):
        """
        :param public_key:
        :type public_key: noise.dh.public.PublicKey
        :param private_key:
        :type private_key: noise.dh.private.PrivateKey
        """
        self._public_key = public_key
        self._private_key = private_key

    @property
    def public(self):
        """
        :return:
        :rtype: noise.dh.public.PublicKey
        """
        return self._public_key

    @property
    def private(self):
        """
        :return:
        :rtype: noise.dh.private.PrivateKey
        """
        return self._private_key
