import os
from PIL import Image, ImageSequence

def image_to_ascii(img, width=200):
    gray_scale = "AOGEV@%#*+=-:,. "
    img = img.convert("L")
    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width * 0.55)
    img = img.resize((width, height))
    pixels = img.getdata()
    chars = ''.join([gray_scale[pixel * (len(gray_scale) - 1) // 255] for pixel in pixels])
    return '\n'.join([chars[i:i + width] for i in range(0, len(chars), width)])

def export_ascii_html(path, output_file="ascii_bird_player.html"):
    img = Image.open(path)
    frames = [image_to_ascii(f.copy()) for f in ImageSequence.Iterator(img)]

    with open(output_file, "w", encoding="utf-8") as f:
        # HTML + CSS + JS Header
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ASCII Bird Animation</title>
    <style>
        body {
            background-color: black;
            color: lightgreen;
            font-family: monospace;
            white-space: pre;
            font-size: 10px;
            padding: 20px;
        }
        #ascii {
            line-height: 1;
        }
    </style>
</head>
<body>
<pre id="ascii"></pre>
<script>
const frames = [
""")

        # Write all frames
        for i, frame in enumerate(frames):
            safe = frame.replace("`", "\\`")
            f.write(f"`{safe}`")
            if i != len(frames) - 1:
                f.write(",\n")
        f.write("""
];
let index = 0; 
setInterval(() => {
    document.getElementById('ascii').textContent = frames[index];
    index = (index + 1) % frames.length;
}, 200);
</script>
</body>
</html>
""")

    print(f"已匯出完整 HTML 檔案到 {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python gif_to_ascii_export_html.py <gif檔案路徑>")
    else:
        export_ascii_html(sys.argv[1])
