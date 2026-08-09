from typing import NewType

RGB8 = tuple[int, int, int]
SRGB = NewType("SRGB", tuple[float, float, float])
LinearRGB = NewType("LinearRGB", tuple[float, float, float])
XYZ = NewType("XYZ", tuple[float, float, float])
LinearLMS = NewType("LinearLMS", tuple[float, float, float])

MAX_CHANNEL_VALUE = 255

# sRGB transfer function constants (IEC 61966-2-1).
SRGB_LINEAR_THRESHOLD = 0.04045
SRGB_LINEAR_SLOPE = 12.92
SRGB_OFFSET = 0.055
SRGB_EXPONENT = 2.4

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

    medium = 

    small = 

