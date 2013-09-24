

#def cacheirator(func):
#    def wrapper(*args):
#        value = mc.get(str(args))
#        if not value:
#            value = func(*args)
#            mc.set(str(args), value, time = 0)
#        return value


def ipv4ToInit(ip):
    result = []
    octs = [int(i) for i in ip.split('.')]

    for i in range(24, -1, -8):
        result.append(octs.pop(0) << i)

    return sum(result)


def intToIpv4(num):
    result = []

    for i in range(24, -1, -8):
        result.append(str((num >> i) & 255))

    return ".".join(result)
