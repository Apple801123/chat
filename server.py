from socket import socket,AF_INET,SOCK_DGRAM
from json import dumps,loads
cliends = {}
i = socket(AF_INET,SOCK_DGRAM)
i.bind(("0.0.0.0",35243))
while True:
    data,addr = i.recvfrom(2048)
    data = data.decode()
    data = loads(data)
    print(data)
    if(data['addr'][0] not in cliends):
        cliends.update({addr[0]:data['addr'][1]})
    if(data['type']=='msg'):
        data=data['user']+" : "+data['msg']
    elif(data['type']=='signup'):
        data=data['user']+"加入了聊天室"
    elif(data['type']=='logout'):
        del cliends[addr[0]]
        data=data['user']+"退出了聊天室"
    print(cliends)
    for ii in cliends:
        print(ii)
        o = socket(AF_INET,SOCK_DGRAM)
        o.sendto(data.encode(),tuple((ii,cliends[ii])))
        o.close()