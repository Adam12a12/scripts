# host side:

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE
sudo iptables -A FORWARD -i wlp3s0 -o usb0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i usb0 -o wlp3s0 -j ACCEPT

# device side:

ip route add default via 172.16.42.2 dev rndis0
setup-interfaces
# edit /etc/resolv.conf file