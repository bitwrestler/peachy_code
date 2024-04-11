#Windows powershell script for forwarding the WSL2 port to all addresses on the local and then opening up the firewall to that port
$port = $(python3 -c "import ServerCommon; print(ServerCommon.LISTEN_IF_PORT)") #must execute from source directory and have python for windows installed
netsh interface portproxy set v4tov4 listenport=$($port) listenaddress=0.0.0.0 connectport=$($port) connectaddress=$(wsl hostname -I)
netsh advfirewall firewall add rule name="Forwarding Peachy Code gRPC Server TCP port $($port)" protocol=TCP dir=in action=allow localport=$($port)