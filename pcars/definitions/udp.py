import enum
import ctypes

PORT = 5606
MAX_PACKET_SIZE = 1500
TYRE_NAME_LENGTH_MAX = 40
PARTICIPANT_NAME_LENGTH_MAX = 64
PARTICIPANTS_PER_PACKET = 16
STREAMER_PARTICIPANTS_SUPPORTED = 32
TRACK_NAME_LENGTH_MAX = 64
VEHICLE_NAME_LENGTH_MAX = 64
CLASS_NAME_LENGTH_MAX = 20
VEHICLES_PER_PACKET = 16
CLASSES_SUPPORTED_PER_PACKET = 60


class StreamerPacketHandlerType(enum.Enum):
    CAR_PHYSICS = 0,
    RACE_DEFINITION = 1,
    PARTICIPANTS = 2,
    TIMINGS = 3,
    GAME_STATE = 4,
    WEATHER_STATE = 5,  # not sent at the moment, information can be found in the game state packet
    VEHICLE_NAMES = 6,  # not sent at the moment
    TIME_STATS = 7,
    PARTICIPANTS_VEHICLE_NAMES = 8


class PackedStructure(ctypes.Structure):
    _pack_ = 1


class PacketBase(PackedStructure):
    _fields_ = [
        ('packet_number', ctypes.c_uint),
        ('category_packet_number', ctypes.c_uint),
        ('partial_packet_index', ctypes.c_ubyte),
        ('partial_packet_number', ctypes.c_ubyte),
        ('packet_type', ctypes.c_ubyte),
        ('packet_version', ctypes.c_ubyte),
    ]


_packet_base = ('packet_base', PacketBase)


class TelemetryData(PackedStructure):
    PACKET_TYPE = 0
    VERSION = 4

    _fields_ = [
        _packet_base,
        ('viewed_participant_index', ctypes.c_char),
        ('unfiltered_throttle', ctypes.c_ubyte),
        ('unfiltered_brake', ctypes.c_ubyte),
        ('unfiltered_steering', ctypes.c_char),
        ('unfiltered_clutch', ctypes.c_ubyte),
        ('car_flags', ctypes.c_ubyte),
        ('oil_temp_celsius', ctypes.c_short),
        ('oil_pressure_kpa', ctypes.c_ushort),
        ('water_temp_celsius', ctypes.c_short),
        ('water_pressure_kpa', ctypes.c_ushort),
        ('fuel_pressure_kpa', ctypes.c_ushort),
        ('fuel_capacity', ctypes.c_ubyte),
        ('brake', ctypes.c_ubyte),
        ('throttle', ctypes.c_ubyte),
        ('clutch', ctypes.c_ubyte),
        ('fuel_level', ctypes.c_float),
        ('speed', ctypes.c_float),
        ('rpm', ctypes.c_ushort),
        ('max_rpm', ctypes.c_ushort),
        ('steering', ctypes.c_char),
        ('gear_num_gears', ctypes.c_ubyte),
        ('boost_amount', ctypes.c_ubyte),
        ('crash_state', ctypes.c_ubyte),
        ('odometer_km', ctypes.c_float),
        ('orientation', ctypes.c_float * 3),
        ('local_velocity', ctypes.c_float * 3),
        ('world_velocity', ctypes.c_float * 3),
        ('angular_velocity', ctypes.c_float * 3),
        ('local_acceleration', ctypes.c_float * 3),
        ('world_acceleration', ctypes.c_float * 3),
        ('extents_centre', ctypes.c_float * 3),
        ('tyre_flags', ctypes.c_ubyte * 4),
        ('terrain', ctypes.c_ubyte * 4),
        ('tyre_y', ctypes.c_float * 4),
        ('tyre_rps', ctypes.c_float * 4),
        ('tyre_temp', ctypes.c_ubyte * 4),
        ('tyre_height_above_ground', ctypes.c_float * 4),
        ('tyre_wear', ctypes.c_ubyte * 4),
        ('brake_damage', ctypes.c_ubyte * 4),
        ('suspension_damage', ctypes.c_ubyte * 4),
        ('brake_temp_celsius', ctypes.c_short * 4),
        ('tyre_tread_temp', ctypes.c_ushort * 4),
        ('tyre_layer_temp', ctypes.c_ushort * 4),
        ('tyre_carcass_temp', ctypes.c_ushort * 4),
        ('tyre_rim_temp', ctypes.c_ushort * 4),
        ('tyre_internal_air_temp', ctypes.c_ushort * 4),
        ('tyre_temp_left', ctypes.c_ushort * 4),
        ('tyre_temp_center', ctypes.c_ushort * 4),
        ('tyre_temp_right', ctypes.c_ushort * 4),
        ('wheel_local_position_y', ctypes.c_float * 4),
        ('ride_height', ctypes.c_float * 4),
        ('suspension_travel', ctypes.c_float * 4),
        ('suspension_velocity', ctypes.c_float * 4),
        ('suspension_ride_height', ctypes.c_ushort * 4),
        ('air_pressure', ctypes.c_ushort * 4),
        ('engine_speed', ctypes.c_float),
        ('engine_torque', ctypes.c_float),
        ('wings', ctypes.c_ubyte * 2),
        ('hand_brake', ctypes.c_ubyte),
        ('aero_damage', ctypes.c_ubyte),
        ('engine_damage', ctypes.c_ubyte),
        ('joy_pad0', ctypes.c_uint),
        ('d_pad', ctypes.c_ubyte),
        ('tyre_compound', (ctypes.c_char * TYRE_NAME_LENGTH_MAX) * 4),
        ('turbo_boost_pressure', ctypes.c_float),
        ('full_position', ctypes.c_float * 3),
        ('brake_bias', ctypes.c_ubyte),
        ('tick_count', ctypes.c_uint),
    ]


class RaceData(PackedStructure):
    PACKET_TYPE = 1
    VERSION = 1

    _fields_ = [
        _packet_base,
        ('world_fastest_lap_time', ctypes.c_float),
        ('personal_fastest_lap_time', ctypes.c_float),
        ('personal_fastest_sector1_time', ctypes.c_float),
        ('personal_fastest_sector2_time', ctypes.c_float),
        ('personal_fastest_sector3_time', ctypes.c_float),
        ('world_fastest_sector1_time', ctypes.c_float),
        ('world_fastest_sector2_time', ctypes.c_float),
        ('world_fastest_sector3_time', ctypes.c_float),
        ('track_length', ctypes.c_float),
        ('track_location', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('track_variation', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('translated_track_location', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('translated_track_variation', ctypes.c_char * TRACK_NAME_LENGTH_MAX),
        ('laps_time_in_event', ctypes.c_ushort),
        ('enforced_pit_stop_lap', ctypes.c_char),
    ]


class ParticipantsData(PackedStructure):
    PACKET_TYPE = 2
    VERSION = 2

    _fields_ = [
        _packet_base,
        ('participants_changed_timestamp', ctypes.c_uint),
        ('name', (ctypes.c_char * PARTICIPANT_NAME_LENGTH_MAX) * PARTICIPANTS_PER_PACKET),
        ('nationality', ctypes.c_uint * PARTICIPANTS_PER_PACKET),
        ('participants_changed_timestamp', ctypes.c_ushort * PARTICIPANTS_PER_PACKET),
    ]


class ParticipantsInfo(PackedStructure):
    VERSION = 3

    _fields_ = [
        ('world_position', ctypes.c_short * 3),
        ('orientation', ctypes.c_short * 3),
        ('current_lap_distance', ctypes.c_ushort),
        ('race_position', ctypes.c_ubyte),
        ('sector', ctypes.c_ubyte),
        ('highest_flag', ctypes.c_ubyte),
        ('pit_mode_schedule', ctypes.c_ubyte),
        ('car_index', ctypes.c_ushort),
        ('race_state', ctypes.c_ubyte),
        ('current_lap', ctypes.c_ubyte),
        ('current_time', ctypes.c_float),
        ('current_sector_time', ctypes.c_float),
        ('participant_index', ctypes.c_ushort),

    ]


class TimingsData(PackedStructure):
    PACKET_TYPE = 3
    VERSION = 2

    _fields_ = [
        _packet_base,
        ('num_participants', ctypes.c_char),
        ('participants_changed_timestamp', ctypes.c_uint),
        ('event_time_remaining', ctypes.c_float),
        ('split_time_ahead', ctypes.c_float),
        ('split_time_behind', ctypes.c_float),
        ('split_time', ctypes.c_float),
        ('partcipants', ParticipantsInfo * STREAMER_PARTICIPANTS_SUPPORTED),
        ('local_participant_index', ctypes.c_ushort),
        ('tick_count', ctypes.c_uint),
    ]


class GameStateData(PackedStructure):
    PACKET_TYPE = 4
    VERSION = 2

    _fields_ = [
        _packet_base,
        ('build_version_number', ctypes.c_ushort),
        ('game_state', ctypes.c_char),
        ('ambient_temperature', ctypes.c_char),
        ('track_temperature', ctypes.c_char),
        ('rain_density', ctypes.c_ubyte),
        ('snow_density', ctypes.c_ubyte),
        ('wind_speed', ctypes.c_char),
        ('wind_direction_x', ctypes.c_char),
        ('wind_direction_y;', ctypes.c_char),
    ]


class ParticipantStatsInfo(PackedStructure):
    VERSION = 2

    _fields_ = [
        ('fastest_lap_time', ctypes.c_float),
        ('last_lap_time', ctypes.c_float),
        ('last_sector_time', ctypes.c_float),
        ('fastest_sector1_time', ctypes.c_float),
        ('fastest_sector2_time', ctypes.c_float),
        ('fastest_sector3_time', ctypes.c_float),
        ('participant_online_rep', ctypes.c_uint),
        ('participant_index', ctypes.c_ushort),
    ]


class ParticipantsStats(PackedStructure):
    VERSION = 2

    _fields_ = [
        ('participants', ParticipantStatsInfo * STREAMER_PARTICIPANTS_SUPPORTED),
    ]


class TimeStatsData(PackedStructure):
    PACKET_TYPE = 7
    VERSION = 2

    _fields_ = [
        _packet_base,
        ('participants_changed_timestamp', ctypes.c_uint),
        ('stats', ParticipantsStats),
    ]


class VehicleInfo(PackedStructure):
    VERSION = 2

    _fields_ = [
        ('index', ctypes.c_ushort),
        ('class', ctypes.c_uint),
        ('name', ctypes.c_char * VEHICLE_NAME_LENGTH_MAX),
    ]


class ParticipantVehicleNamesData(PackedStructure):
    VERSION = 2

    _fields_ = [
        _packet_base,
        ('vehicles', VehicleInfo * VEHICLES_PER_PACKET),
    ]


class ClassInfo(PackedStructure):
    VERSION = 2

    _fields_ = [
        ('class_index', ctypes.c_uint),
        ('name', ctypes.c_char * CLASS_NAME_LENGTH_MAX),
    ]


class VehicleClassNamesData(PackedStructure):
    VERSION = 2

    _fields_ = [
        _packet_base,
        ('classes', ClassInfo * CLASSES_SUPPORTED_PER_PACKET),
    ]
