def receive_udp_packet():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.bind(('', 5606))
        content, _ = sock.recvfrom(4096)
        return content


