





Tracert baidui.com





![1651290577146](C:\Users\Anita\AppData\Roaming\Typora\typora-user-images\1651290577146.png)





10.5.1.0  255.255.0.0  192.168.80.1  

10.5.6.0  255.255.0.0  192.168.80.1  192.168.80.10 2





route delete 0.0.0.0

route add 10.5.0.0 mask 255.255.0.0 192.168.80.1 -p

route add 10.5.5.0 mask 255.255.255.0 192.168.80.1 -p



route print

route delete 0.0.0.0

route add 0.0.0.0 mask 0.0.0.0 10.10.30.1 -p

route add 10.5.0.0 mask 255.255.0.0 192.168.80.1 -p