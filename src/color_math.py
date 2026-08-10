'''
color_math.py
'''

from typing import NewType
import math

RGB8            = NewType("RGB8", tuple[int, int, int])
SRGB            = NewType("SRGB", tuple[float, float, float])
LinearRGB       = NewType("LinearRGB", tuple[float, float, float])
XYZ             = NewType("XYZ", tuple[float, float, float])
LinearLMS       = NewType("LinearLMS", tuple[float, float, float])
NonLinearLMS    = NewType("NonLinearLMS", tuple[float, float, float])
Oklab           = NewType("Oklab", tuple[float, float, float])
OKLCH           = NewType("OKLCH", tuple[float, float, float])

MAX_CHANNEL_VALUE = 255

# sRGB transfer function constants (IEC 61966-2-1).
SRGB_LINEAR_THRESHOLD = 0.04045
SRGB_LINEAR_SLOPE = 12.92
SRGB_OFFSET = 0.055
SRGB_EXPONENT = 2.4

CHROMA_EPSILON = 1e-8

_HEX_DIGITS = frozenset("0123456789abcdefABCDEF")


def canonicalize_hex(hex_code: str) -> str:
    cleaned = hex_code.removeprefix("#")

    if len(cleaned) == 3:
        cleaned = "".join(ch * 2 for ch in cleaned)

    if len(cleaned) != 6:
        raise ValueError(f"expected 3 or 6 hex digits, got {hex_code!r}")
    if not _HEX_DIGITS.issuperset(cleaned):
        raise ValueError(f"expected only hex digits, got {hex_code!r}")

    return cleaned


def parse_hex_rgb(hex_code: str) -> RGB8:
    color_int = int(canonicalize_hex(hex_code), 16)

    return (
        (color_int >> 16) & 0xFF,
        (color_int >> 8) & 0xFF,
        color_int & 0xFF,
    )


def byte_to_unit(value: int) -> float:
    return value / MAX_CHANNEL_VALUE


def unit_to_byte(value: float) -> int:
    return round(value * MAX_CHANNEL_VALUE)


def srgb_to_linear(encoded: float) -> float:
    if encoded <= SRGB_LINEAR_THRESHOLD:
        return encoded / SRGB_LINEAR_SLOPE
    return ((encoded + SRGB_OFFSET) / (1 + SRGB_OFFSET)) ** SRGB_EXPONENT


def linear_to_srgb(linear: float) -> float:
    if linear <= 0.0031308:
        return SRGB_LINEAR_SLOPE * linear
    return (1 + SRGB_OFFSET) * linear ** (1 / SRGB_EXPONENT) - SRGB_OFFSET


def hex_to_srgb(hex_code: str) -> SRGB:
    red, green, blue = (byte_to_unit(c) for c in parse_hex_rgb(hex_code))
    return SRGB((red, green, blue))


def srgb_to_linear_rgb(rgb: SRGB) -> LinearRGB:
    red, green, blue = (srgb_to_linear(value) for value in rgb)
    return LinearRGB((red, green, blue))


def linear_rgb_to_srgb(rgb: LinearRGB) -> SRGB:
    red, green, blue = (linear_to_srgb(value) for value in rgb)
    return SRGB((red, green, blue))


def linear_rgb_to_xyz(rgb: LinearRGB) -> XYZ:
    red, green, blue = rgb

    x = (
        0.4123907992659595 * red
        + 0.3575843393838780 * green
        + 0.1804807884018343 * blue
    )

    y = (
        0.2126390058715104 * red
        + 0.7151686787677559 * green
        + 0.0721923153607337 * blue
    )

    z = (
        0.0193308187155918 * red
        + 0.1191947797946259 * green
        + 0.9505321522496608 * blue
    )

    return XYZ((x, y, z))


def xyz_to_linear_rgb(xyz: XYZ) -> LinearRGB:
    x, y, z = xyz

    red = (
        3.2409699419045213 * x
        - 1.5373831775700935 * y
        - 0.4986107602930033 * z
    )

    green = (
        -0.9692436362808798 * x
        + 1.8759675015077206 * y
        + 0.0415550574071756 * z
    )

    blue = (
        0.0556300796969936 * x
        - 0.2039769588889765 * y
        + 1.0569715142428786 * z
    )

    return LinearRGB((red, green, blue))


def xyz_to_linear_lms(xyz: XYZ) -> LinearLMS:
    x, y, z = xyz

    long = (
        0.8189330101 * x
        + 0.3618667424 * y
        - 0.1288597137 * z
    )

    medium = (
        0.0329845436 * x
        + 0.9293118715 * y
        + 0.0361456387 * z
    )

    small = (
        0.0482003018 * x
        + 0.2643414314 * y
        + 0.6338517070 * z
    )

    return LinearLMS((long, medium, small))


def linear_lms_to_nonlinear(lms: LinearLMS) -> NonLinearLMS:
    large, medium, small = (channel ** 1/3 for channel in lms)
    return NonLinearLMS((large, medium, small))


def nonlinear_lms_to_oklab(lms: NonLinearLMS) -> Oklab:
    l, m, s = lms

    lightness = (
        0.2104542553 * l
        + 0.7936177850 * m
        - 0.0040720402 * s
    )

    green_red = (
        1.9779984951 * l
        - 2.4285922050 * m
        + 0.4505937099 * s
    )

    blue_yellow = (
        0.0259040371 * l
        + 0.7827717662 * m
        - 0.8086757660 * s
    )

    return Oklab((lightness, green_red, blue_yellow))


def oklab_to_oklch(oklab_rectangle: Oklab) -> OKLCH:
    l, a, b = oklab_rectangle

    chroma = math.hypot(a, b)
    if chroma < CHROMA_EPSILON:
        return OKLCH((l, 0.0, 0.0))
    hue = math.degrees(math.atan2(b, a)) % 360
    return OKLCH((l, chroma, hue))
