# _*_ coding:utf-8 _*_

import ipaddress


def gen_ip_from_network(network):
    """通过给定的网络和掩码生成可用的ip地址列表.
       例如: '10.10.10.0/24'
    """
    network = ipaddress.ip_network(network)
    return [str(ip) for ip in network.hosts()]


if __name__ == '__main__':
    print(gen_ip_from_network('10.10.10.0/24'))
