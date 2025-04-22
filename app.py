from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form fields
        name = request.form['name']
        abilities = request.form['abilities']
        bottom_text = request.form['bottom_text']
        blue = request.form['blue']
        green = request.form['green']
        initiative = request.form['initiative']
        attack = request.form['attack']
        health = request.form['health']
        picture = request.files['picture']

        # Load the uploaded image
        # Use new background dimensions
        card_w, card_h = 336, 500
        try:
            bg = Image.open('background.png').convert('RGBA')
            bg = bg.resize((card_w, card_h))
        except Exception as e:
            bg = Image.new('RGBA', (card_w, card_h), (30,30,30,255))
        card = bg.copy()
        draw = ImageDraw.Draw(card)

        # Place card art (picture) in the large art frame area (20,60) size 296x140
        img = Image.open(picture).convert('RGBA')
        img = img.resize((306, 165))
        card.paste(img, (15, 100), mask=img)


        # Fonts - use Xolonium-Regular.ttf if available, else Starcraft, else default
        try:
            font_title = ImageFont.truetype("Xolonium-Regular.ttf", 30)
            font_abilities = ImageFont.truetype("Xolonium-Regular.ttf", 16)
            font_stats = ImageFont.truetype("Xolonium-Regular.ttf", 20)
            font_bottom = ImageFont.truetype("Xolonium-Regular.ttf", 15)
        except:
            try:
                font_title = ImageFont.truetype("Starcraft Normal.ttf", 30)
                font_abilities = ImageFont.truetype("Starcraft Normal.ttf", 16)
                font_stats = ImageFont.truetype("Starcraft Normal.ttf", 20)
                font_bottom = ImageFont.truetype("Starcraft Normal.ttf", 15)
            except:
                font_title = font_abilities = font_stats = font_bottom = ImageFont.load_default()

        # Helper to draw outlined text
        def draw_outlined_text(draw, pos, text, font, fill, outline_color, anchor="mm"):
            x, y = pos
            # Draw outline
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx != 0 or dy != 0:
                        draw.text((x+dx, y+dy), text, font=font, fill=outline_color, anchor=anchor)
            draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

        # Blue cost (5px up)
        draw_outlined_text(draw, (37, 27), str(blue), font_stats, (0,180,255,255), (0,0,0,255))
        # Name (fixed coordinate)
        draw_outlined_text(draw, (150, 27), name, font_title, (255,255,255,255), (0,0,0,255))
        # Green cost (5px up)
        draw_outlined_text(draw, (292, 27), str(green), font_stats, (0,255,80,255), (0,0,0,255))

        # Abilities (left-aligned, multiline, at 10,320)
        abilities_fixed = abilities.replace('\r\n', '\n').replace('\r', '\n')
        ab_x, ab_y = 10, 320
        max_lines = 5
        for i, line in enumerate(abilities_fixed.split('\n')[:max_lines]):
            draw_outlined_text(draw, (ab_x, ab_y + i*22), line[:40], font_abilities, (220,255,255,255), (0,0,0,255), anchor="la")

        # Attack
        draw_outlined_text(draw, (10+25, 440+25), str(attack), font_stats, (255,100,60,255), (0,0,0,255))
        # Health
        draw_outlined_text(draw, (75+25, 440+25), str(health), font_stats, (255,60,120,255), (0,0,0,255))
        # Initiative
        draw_outlined_text(draw, (275+25, 440+25), str(initiative), font_stats, (255,255,0,255), (0,0,0,255))

        # Bottom text (fixed coordinate)
        draw_outlined_text(draw, (190, 470), bottom_text, font_bottom, (180,220,255,255), (0,0,0,255))


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
