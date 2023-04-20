def color_to_rgb(color):
    return color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF


def rgb_to_color(rgb):
    return (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]


def uint8_to_uduty16(i):
    return int((-65535 / 255) * i + 65535)


def uduty16_to_uint8(d):
    return int((-255 / 65535) * d + 255)
