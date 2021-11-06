"""Decoder/encoder functions for Toio BLE communication messages"""

from struct import pack, unpack
from typing import List, Union
import logging

from .data import *


def _wrongBytesError(data: bytes) -> ValueError:
    raise ValueError("Wrong bytes '%s'" % data)


def decodeToioID(data: bytes) -> Union[PositionID, StandardID, MissedID]:
    if data[0] == 0x01:
        (_, x, y, a, sx, sy, sa) = unpack("<BHHHHHH", data)
        return PositionID(x, y, a, sx, sy, sa)
    if data[0] == 0x02:
        (_, value, angle) = unpack("<BIH", data)
        return StandardID(value, angle)
    if data[0] == 0x03:
        return MissedID(ToioIDType.POSITION)
    if data[0] == 0x04:
        return MissedID(ToioIDType.STANDARD)
    if data[0] == 0xff:
        return MissedID(ToioIDType.INVALID)

    raise _wrongBytesError(data)


def decodeMotion(data: bytes) -> Motion:
    if data[0] == 0x01:
        if len(data) == 3:
            (_, isLevel, collision) = unpack("<BBB", data)
            return Motion(isLevel != 0, collision != 0, False, Orientation.INVALID)
        else:
            (_, isLevel, collision, doubleTap, orientation, shake) = unpack("<BBBBBB", data)
            return Motion(isLevel != 0, collision != 0, doubleTap != 0, Orientation(orientation), shake)
    if data[0] == 0x02:
        (_, status, strength, x, y, z) = unpack("<BBBbbb", data)
        return MagneticForce(status, strength, x, y, z)
    if data[0] == 0x03:
        if data[1] == 0x01:
            (_, angleType, roll, pitch, yaw) = unpack("<BBhhh", data)
            return TiltEuler(roll, pitch, yaw)
        if data[1] == 0x02:
            (_, angleType, w, x, y, z) = unpack("<BBhhhh", data)
            return TiltQuaternion(w, x, y, z)

    raise _wrongBytesError(data)


def decodeButton(data: bytes) -> bool:
    if data[0] == 0x01:
        (_, isPressed) = unpack("<BB", data)
        return isPressed != 0

    raise _wrongBytesError(data)


def decodeBattery(data: bytes) -> int:
    return unpack("<B", data)[0]


def _motorDirection(value: int) -> int:
    return 1 if value >= 0 else 2

def decodeMotor(data: bytes) -> Motor:
    if len(data) == 3:
        return(Motor(data[0], data[1], data[2]))
    raise _wrongBytesError(data)

def encodeMotor(left: int, right: int, duration: float = 0) -> bytes:
    d = min(int(duration * 100), 255)
    return bytes([2, 1, _motorDirection(left), abs(left), 2, _motorDirection(right), abs(right), d])

def encodeMotorTarget(ctrlid: int, x: int, y: int, timeout: int = 0, movingtype: int = 0, maxspeed: int = 0, speedtype: int = 0,  angletype: int = 5, deg: int = 0) -> bytes:
    id = min(ctrlid, 255)
    t = min(timeout, 255)
    mt = min(movingtype, 2)
    ms = min(maxspeed, 255)
    st = min(speedtype, 3)
    a = (angletype << 13) | (deg & 0x1ffff)
    return bytes([3, id, t, mt, ms, st, 0]) + x.to_bytes(2, 'little') + y.to_bytes(2, 'little') + a.to_bytes(2, 'little')

def encodeMotorMultipleTargets(ctrlid: int, goals, writemode: int = 0,  timeout: int = 0, movingtype: int = 0, maxspeed: int = 0, speedtype: int = 0) -> bytes:
    id = min(ctrlid, 255)
    wm = min(writemode, 1)
    t = min(timeout, 255)
    mt = min(movingtype, 2)
    ms = min(maxspeed, 255)
    st = min(speedtype, 3)
    goallist = bytes()
    for goal in goals:
        x = goal[0]
        y = goal[1]
        angletype = goal[2]
        deg = goal[3]
        a = (angletype << 13) | (deg & 0x1ffff)
        goallist = goallist + x.to_bytes(2, 'little') + y.to_bytes(2, 'little') + a.to_bytes(2, 'little')
        if len(goallist) > 29:
            print('too many goal positions')
            return 0
    return bytes([4, id, t, mt, ms, st, 0, wm]) + goallist

def encodeMotorAcceleration(transspeed: int, transaccel: int,  turnspeed: int, turndirection: int, traveldirection: int = 0, priority:int = 0, duration: float = 0) -> bytes:
    ts = min(transspeed, 115)
    ta = min(transaccel, 255)
    tns = min(turnspeed, 65535)
    tnd = min(turndirection, 1)
    trvd = min(traveldirection, 1)
    d = min(int(duration * 100), 255)
    p = min(priority, 1)
    return bytes([5, ts, ta]) + tns.to_bytes(2, 'little') + bytes([tnd, trvd, p, d])

def encodeLight(r: int, g: int, b: int, duration: float = 0) -> bytes:
    return bytes([3, min(int(duration * 100), 255), 1, 1, r, g, b])


def encodeLightPattern(lights: List[Light], repeat: int = 0) -> bytes:
    b = list([4, repeat, len(lights)])
    for light in lights:
        b += [min(int(light.duration * 100), 255), 1, 1, light.r, light.g, light.b]
    return bytes(b)


def encodeLightOff() -> bytes:
    return bytes([1])


def encodeSound(id: int, volume: int = 255) -> bytes:
    return bytes([2, id, volume])


def encodeSoundByNotes(notes: List[Note], repeat: int = 0) -> bytes:
    b = list([3, repeat, len(notes)])
    for note in notes:
        b += [min(int(note.duration * 100), 255), note.noteNumber, note.volume]
    return bytes(b)


def encodeSoundOff() -> bytes:
    return bytes([1])


def encodeConfigProtocolVersionRequest() -> bytes:
    return bytes([1, 0])


def decodeConfigProtocolVersionResponse(data: bytes) -> str:
    if data[0] == 0x81:
        return data[2:].decode()
    raise _wrongBytesError(data)


def encodeConfigLevelThreshold(angle: int = 45) -> bytes:
    return bytes([5, 0, min(angle, 45)])


def encodeConfigCollisionThreshold(value: int = 7) -> bytes:
    return bytes([6, 0, min(value, 10)])


def encodeConfigDoubleTapTiming(value: int = 5) -> bytes:
    return bytes([0x17, 0, min(value, 7)])


def encodeConfigToioIDNotify(duration: float = 0.1, condition: int = 0xff) -> bytes:
    return bytes([0x18, 0, min(int(duration * 100), 255), condition])


def encodeConfigToioIDMissedNotify(delay: float = 0.7) -> bytes:
    return bytes([0x19, 0, min(int(delay * 100), NotifyType.CHANGEDOR300MS)])


def encodeConfigMagneticSensor(capability: int = MagneticSenseType.DISABLE, duration: float = 0, condition: int = NotifyType.CHANGED) -> bytes:
    return bytes([0x1b, 0, capability,
                  min(int(duration * 50), 255), condition])


def encodeConfigMotorSpeedNotify(enable: int = 1) -> bytes:
    return bytes([0x1c, 0, min(enable, 1)])


def encodeConfigHighPrecisionTiltSensor(type: int = AngleType.EULER, duration: float = 0, condition = NotifyType.CHANGED) -> bytes:
    return bytes([0x1d, 0, type, min(int(duration * 100), 255), condition])