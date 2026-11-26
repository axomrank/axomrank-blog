"""Render AxomRank social cards for published guides."""
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
PAPER = "#fcfaf7"
MAROON = "#80151a"
INK = "#272222"
DEFAULT_TITLE_FONT = "DejaVuSerif.ttf"
ASSAMESE_TITLE_FONT = "NotoSerifBengali-Regular.ttf"


def wrap_title(title, font, max_width):
    lines = []
    line = ""
    for word in title.split():
        candidate = f"{line} {word}".strip()
        if line and font.getlength(candidate) > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def render(post, path):
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 15, HEIGHT), fill=MAROON)
    draw.text((82, 80), "AxomRank Blog", fill=MAROON,
              font=ImageFont.truetype("DejaVuSans-Bold.ttf", 33))
    draw.line((82, 151, 1118, 151), width=2, fill="#ded5cc")
    font_name = ASSAMESE_TITLE_FONT if post.get("lang", "").startswith("as") else DEFAULT_TITLE_FONT
    for size in range(69, 30, -2):
        font = ImageFont.truetype(font_name, size)
        lines = wrap_title(post["title"], font, max_width=1036)
        if len(lines) * (size + 17) <= 360 and all(font.getlength(line) <= 1036 for line in lines):
            break
    else:
        raise ValueError(f"{post['slug']}: title does not fit its social preview")

    draw.multiline_text((82, 184), "\n".join(lines), font=font, fill=INK, spacing=12)
    draw.line((82, 542, 1118, 542), width=2, fill="#ded5cc")
    draw.text((82, 567), "Free preparation for Assam government exams", fill=MAROON,
              font=ImageFont.truetype("DejaVuSans.ttf", 23))
    image.save(path, quality=88, optimize=True)
