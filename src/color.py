from slint import Color


def oklab_to_rgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ * l_ * l_
    m = m_ * m_ * m_
    s = s_ * s_ * s_

    r_lin = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g_lin = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b_lin = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def lin_to_srgb(c):
        if c <= 0.0031308:
            return 12.92 * c
        return 1.055 * (c ** (1.0 / 2.4)) - 0.055

    r = max(0.0, min(1.0, lin_to_srgb(r_lin)))
    g = max(0.0, min(1.0, lin_to_srgb(g_lin)))
    b = max(0.0, min(1.0, lin_to_srgb(b_lin)))

    return (r, g, b)


def oklab_to_rgb_int(L, a, b):
    r, g, b_float = oklab_to_rgb(L, a, b)
    return (round(r * 255), round(g * 255), round(b_float * 255))


def hex_to_slint_color(hex: str) -> Color:
    return Color(
        {
            "red": int(hex[1:3], 16),
            "green": int(hex[3:5], 16),
            "blue": int(hex[5:7], 16),
        }
    )


def dec_to_slint_color(decimal: int) -> Color:
    return Color(
        {
            "red": (decimal >> 16) & 0xFF,
            "green": (decimal >> 8) & 0xFF,
            "blue": decimal & 0xFF,
        }
    )


def fg_rgb(text, r, g, b) -> str:
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def bg_rgb(text, r, g, b) -> str:
    return f"\033[48;2;{r};{g};{b}m{text}\033[0m"


if __name__ == "__main__":
    print(fg_rgb("This is a custom coral/pink color!", 255, 127, 80))
    print(bg_rgb("This has a custom mint green background!", 152, 251, 152))
