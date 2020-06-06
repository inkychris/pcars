import pcars.sms.udp as sms_udp
import socket


class udp_socket:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.bind(('', sms_udp.PORT))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()

    def receive(self):
        return self._socket.recvfrom(sms_udp.MAX_PACKET_SIZE)[0]


class Telemetry:
    def __init__(self):
        self._vehicle_data = _VehicleData()

    @staticmethod
    def _assert_packet_version(struct, version):
        if version != struct.VERSION:
            raise ValueError(f'invalid packet version {version}, expected {struct.VERSION}')

    def update_from_udp(self, udp_packet):
        base_packet = sms_udp.PacketBase.from_buffer_copy(udp_packet)
        if base_packet.packet_type == sms_udp.TelemetryData.PACKET_TYPE:
            self._assert_packet_version(sms_udp.TelemetryData, base_packet.packet_version)
            self._vehicle_data.update_from_udp(udp_packet)

    @property
    def vehicle(self):
        return self._vehicle_data


class _BaseData:
    _udp_struct = None

    def __init__(self):
        self._last_udp_packet = None

    def _udp_packet_property(self, property):
        if self._last_udp_packet is None:
            raise ValueError('UDP packet data not available')
        return getattr(self._udp_struct.from_buffer_copy(self._last_udp_packet), property)

    def update_from_udp(self, udp_packet):
        self._last_udp_packet = udp_packet

    @property
    def packet_number(self):
        return self._udp_packet_property('packet_base').packet_number

    @property
    def category_packet_number(self):
        return self._udp_packet_property('packet_base').category_packet_number

    @property
    def partial_packet_index(self):
        return self._udp_packet_property('packet_base').partial_packet_index

    @property
    def partial_packet_number(self):
        return self._udp_packet_property('packet_base').partial_packet_number


class _VehicleData(_BaseData):
    _udp_struct = sms_udp.TelemetryData

    @property
    def speed(self):
        return self._last_udp_packet('speed')

    @property
    def rpm(self):
        return self._last_udp_packet('rpm')
