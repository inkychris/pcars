import pcars.definitions.udp as udp_defs
import socket


class udp_socket:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.bind(('', udp_defs.PORT))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()

    def receive(self):
        return self._socket.recvfrom(udp_defs.MAX_PACKET_SIZE)[0]


class PacketTypeError(Exception):
    pass


class Telemetry:
    def __init__(self):
        self._vehicle_data = _VehicleData()
        self._race_data = _RaceData()
        self._participants_data = _ParticipantsData()
        self._timings_data = _TimingsData()
        self._game_state_data = _GameStateData()
        self._time_stats_data = _TimeStatsData()
        self._participants_vehicle_names_data = _ParticipantVehicleNamesData()

        self._data = (
            self._vehicle_data,
            self._race_data,
            self._participants_data,
            self._timings_data,
            self._game_state_data,
            self._time_stats_data,
            self._participants_vehicle_names_data
        )

    @staticmethod
    def _assert_packet_version(struct, version):
        if version != struct.VERSION:
            raise ValueError(f'invalid packet version {version}, expected {struct.VERSION}')

    def update_from_udp(self, udp_packet):
        packet_base = udp_defs.PacketBase.from_buffer_copy(udp_packet)
        success = False
        for data_type in self._data:
            try:
                data_type._update_from_udp(packet_base, udp_packet)
                break
            except PacketTypeError:
                pass
        if not success:
            raise PacketTypeError(f'unrecognised packet type {packet_base.packet_type}')

    @property
    def vehicle(self):
        return self._vehicle_data


class _BaseData:
    _udp_struct = None

    def __init__(self):
        self._last_udp_packet = None

    def _update_from_udp(self, packet_base, udp_packet):
        if packet_base.packet_type != self._udp_struct.PACKET_TYPE:
            raise PacketTypeError(
                f'expected packet type {self._udp_struct.PACKET_TYPE}, got {packet_base.packet_type}')
        self._last_udp_packet = udp_packet

    def _udp_packet_property(self, property, cast=None):
        if self._last_udp_packet is None:
            return None
        value = getattr(self._udp_struct.from_buffer_copy(self._last_udp_packet), property)
        if value is None:
            return None
        if cast is None:
            return value
        return cast(value)

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
    _udp_struct = udp_defs.TelemetryData

    @property
    def speed(self):
        return self._udp_packet_property('speed')

    @property
    def rpm(self):
        return self._udp_packet_property('rpm')


class _RaceData(_BaseData):
    _udp_struct = udp_defs.RaceData

    @property
    def track_location(self):
        val = self._udp_packet_property('track_location')
        if val:
            return bytes(val).decode('utf-8')


class _ParticipantsData(_BaseData):
    _udp_struct = udp_defs.ParticipantsData

    @property
    def name(self):
        val = self._udp_packet_property('name')
        if val:
            return bytes(val).decode('utf-8')


class _TimingsData(_BaseData):
    _udp_struct = udp_defs.TimingsData

    @property
    def participant_count(self):
        val = self._udp_packet_property('num_participants')
        if val:
            return int.from_bytes(val, byteorder='little')


class _GameStateData(_BaseData):
    _udp_struct = udp_defs.GameStateData

    @property
    def track_temperature(self):
        val = self._udp_packet_property('track_temperature')
        if val:
            return int.from_bytes(val, byteorder='little')


class _TimeStatsData(_BaseData):
    _udp_struct = udp_defs.TimeStatsData

    @property
    def stats(self):
        return self._udp_packet_property('stats')


class _ParticipantVehicleNamesData(_BaseData):
    _udp_struct = udp_defs.ParticipantVehicleNamesData

    @property
    def vehicles(self):
        val = self._udp_packet_property('vehicles')
        if val:
            return val[0].name
