from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        import csv
        # Check for import file
        import_file = request.files.get('import_file')
        if import_file and import_file.filename:
            # Parse first line of CSV
            line = import_file.read().decode('utf-8').strip().splitlines()[0]
            reader = csv.reader([line])
            row = next(reader)
            # Unpack with defaults
            (name, cost, time, atk_hp, armor, r, g, origin, reqs, comment) = tuple(list(row) + ['']*max(0,10-len(row)))
            # Split cost and atk_hp
            blue, green = (cost.split('/')+[0,0])[:2]
            attack, health = (atk_hp.split('/')+[0,0])[:2]
            abilities = f"{origin}\n{reqs}\n{comment}"
            bottom_text = ''
            picture = request.files.get('picture')
        else:
            # Get form fields
            name = request.form['name']
            abilities = request.form['abilities']
            bottom_text = request.form['bottom_text']
            blue = request.form['blue']
            green = request.form['green']
            armor = request.form['armor']
            time = request.form['time']
            attack = request.form['attack']
            health = request.form['health']
            r = request.form.get('r','')
            g = request.form.get('g','')
            picture = request.files['picture']
        # If not set (import), try to get r/g from parsed row
        r = r if 'r' in locals() else ''
        g = g if 'g' in locals() else ''

        # Use new background dimensions
        card_w, card_h = 336, 500
        try:
            bg = Image.open('background.png').convert('RGBA').resize((card_w, card_h))
        except Exception as e:
            bg = Image.new('RGBA', (card_w, card_h), (30,30,30,255))
        card = bg.copy()
        draw = ImageDraw.Draw(card)

        # Place card art (picture) in the large art frame area (20,60) size 296x140
        img = Image.open(picture).convert('RGBA').resize((260, 150))
        card.paste(img, (18, 110), mask=img)

        # Fonts - use Xolonium-Regular.ttf if available, else Starcraft, else default
        def get_font(size):
            try:
                return ImageFont.truetype("Xolonium-Regular.ttf", size)
            except:
                try:
                    return ImageFont.truetype("Starcraft Normal.ttf", size)
                except:
                    return ImageFont.load_default()
        font_title = get_font(30)
        font_abilities = get_font(16)
        font_stats = get_font(20)
        font_bottom = get_font(15)

        # Helper: find max font size to fit text in box
        def fit_text(text, box_w, box_h, max_font_size, min_font_size=8, multiline=False, max_lines=1):
            for size in range(max_font_size, min_font_size-1, -1):
                font = get_font(size)
                if multiline:
                    lines = text.split('\n')[:max_lines]
                    heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines]
                    total_h = sum(heights)
                    max_w = max([font.getlength(line) for line in lines] + [1])
                    if total_h <= box_h and max_w <= box_w:
                        return font, size
                else:
                    bbox = font.getbbox(text)
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                    if w <= box_w and h <= box_h:
                        return font, size
            return get_font(min_font_size), min_font_size


        # Helper to draw outlined text
        def draw_outlined_text(draw, pos, text, font, fill, outline_color, anchor="mm"):
            x, y = pos
            # Draw outline
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), text, font=font, fill=outline_color, anchor=anchor)
            draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

        # Word wrap helper (moved up so it's available for name, abilities, bottom text)
        def wrap_text(text, font, max_width):
            lines = []
            for paragraph in text.split('\n'):
                words = paragraph.split()
                if not words:
                    lines.append('')
                    continue
                line = words[0]
                for word in words[1:]:
                    test_line = f"{line} {word}"
                    if font.getlength(test_line) <= max_width:
                        line = test_line
                    else:
                        lines.append(line)
                        line = word
                lines.append(line)
            return lines

        # Blue cost (5px up)
        draw_outlined_text(draw, (37, 27), str(blue), font_stats, (0,180,255,255), (0,0,0,255))
        # Name (fixed box, with word wrap)
        name_x, name_y = 168, 30  # Center of name box
        name_box_w, name_box_h = 170, 38
        font_name, _ = fit_text(name, name_box_w, name_box_h, 34, 12)
        name_lines = wrap_text(name, font_name, name_box_w)
        name_line_height = font_name.getbbox('Ag')[3] - font_name.getbbox('Ag')[1]
        total_name_height = len(name_lines) * name_line_height
        name_start_y = name_y - total_name_height // 2 + name_line_height // 2
        for i, line in enumerate(name_lines):
            draw_outlined_text(draw, (name_x, name_start_y + i * name_line_height), line, font_name, (255,255,255,255), (0,0,0,255))
        # Green cost (5px up)
        draw_outlined_text(draw, (292, 27), str(green), font_stats, (0,255,80,255), (0,0,0,255))

        # Word wrap helper for abilities
        def wrap_text(text, font, max_width):
            lines = []
            for paragraph in text.split('\n'):
                words = paragraph.split()
                if not words:
                    lines.append('')
                    continue
                line = words[0]
                for word in words[1:]:
                    test_line = f"{line} {word}"
                    if font.getlength(test_line) <= max_width:
                        line = test_line
                    else:
                        lines.append(line)
                        line = word
                lines.append(line)
            return lines

        # Abilities (fixed box, with word wrap)
        ab_x, ab_y = 20, 320
        ab_box_w, ab_box_h = 270, 110
        max_lines = 15
        font_ab, _ = fit_text(abilities, ab_box_w, ab_box_h, 20, 10, multiline=True, max_lines=max_lines)
        lines = wrap_text(abilities, font_ab, ab_box_w)[:max_lines]
        line_height = font_ab.getbbox('Ag')[3] - font_ab.getbbox('Ag')[1]
        for i, line in enumerate(lines):
            draw_outlined_text(draw, (ab_x, ab_y + i*line_height), line, font_ab, (220,255,255,255), (0,0,0,255), anchor="la")

        # Bottom text (fixed box, with word wrap)
        bottom_text_x, bottom_text_y = 140, 460
        bottom_box_w, bottom_box_h = 130, 50
        font_bot, _ = fit_text(bottom_text, bottom_box_w, bottom_box_h, 18, 8)
        bot_lines = wrap_text(bottom_text, font_bot, bottom_box_w)
        bot_line_height = font_bot.getbbox('Ag')[3] - font_bot.getbbox('Ag')[1]
        total_bot_height = len(bot_lines) * bot_line_height
        bot_start_y = bottom_text_y - total_bot_height // 2 + bot_line_height // 2
        for i, line in enumerate(bot_lines):
            draw_outlined_text(draw, (bottom_text_x, bot_start_y + i * bot_line_height), line, font_bot, (180,220,255,255), (0,0,0,255))

        # Attack
        draw_outlined_text(draw, (10+25, 440+25), str(attack), font_stats, (255,100,60,255), (0,0,0,255))
        # Health
        draw_outlined_text(draw, (305, 440+25), str(health), font_stats, (255,60,120,255), (0,0,0,255))
        # Armor
        draw_outlined_text(draw, (240, 440+25), str(armor), font_stats, (255,255,0,255), (0,0,0,255))
        # Time (bottom far right)
        draw_outlined_text(draw, (290, 75), str(time), font_stats, (120,220,255,255), (0,0,0,255))
        # R and G
        draw_outlined_text(draw, (291, 180), r, font_stats, (255,255,255,255), (0,0,0,255))
        draw_outlined_text(draw, (291, 227), g, font_stats, (255,255,255,255), (0,0,0,255))



        # Output image
        img_io = io.BytesIO()
        card.save(img_io, format='PNG')
        img_io.seek(0)
        if 'preview' in request.form and request.form['preview'] == '1':
            # Show preview inline
            return send_file(img_io, mimetype='image/png', as_attachment=False)
        else:
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='card.png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
