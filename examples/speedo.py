import pcars

telemetry = pcars.Telemetry()

with pcars.udp_socket() as socket:
    while True:
        telemetry.update_from_udp(socket.receive())
        print(f'\rspeed: {telemetry.vehicle.speed}', end='')
