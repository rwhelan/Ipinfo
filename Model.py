
import Controller

class OrgRecord(object):
    def __init__(self, ip):
        self.ip = ip

        self._asn = Controller.getAS(self.ip)
        self._org = Controller.getLocation(self.ip)
    
        for k, v in zip( ('_locid',
                          'country',
                          'region',
                          'city',
                          'postalCode',
                          'latitude',
                          'longitude',
                          'metroCode',
                          'areaCode'),
                          self._org ):

            self.__setattr__(k, v)

        if self._asn.startswith('AS'):
            self.asnum, self.orgname = self._asn.split(' ', 1)
        else:
            self.asnum, self.orgname = ('', '')

    def __iter__(self):
        self._iters = [i for i in dir(self) if not i.startswith('_')]
        self._iters.remove('next')

        return self

    def next(self):
        if len(self._iters) == 0:
            raise StopIteration

        _key = self._iters.pop(0)
        return (_key, getattr(self, _key))
