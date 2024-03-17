from flask import Flask, send_file, request
import os
from io import BytesIO
from easy_pil import Canvas, Editor, Font, Text
import requests

app = Flask(__name__)

# Vérifier si le dossier "output" existe, sinon le créer
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

@app.route('/generate_profile_card', methods=['GET'])
def generate_profile_card():
    # Récupérer les données de l'utilisateur depuis l'URL
    name = request.args.get('name', 'John Doe')
    xp = request.args.get('xp', '1.2k')
    next_level_xp = request.args.get('next_level_xp', '5k')
    level = request.args.get('level', '5')
    percentage = int(request.args.get('percentage', 45))
    rank = int(request.args.get('rank', 9))
    profile_image_url = request.args.get('profile_image_url', 'https://example.com/default_profile_image.png')

    # Télécharger l'image de profil depuis l'URL
    response = requests.get(profile_image_url)
    profile_image = BytesIO(response.content)

    background = Editor(Canvas((934, 282), color="#23272a"))
    profile = Editor(profile_image).resize((190, 190)).circle_image()

    poppins = Font.poppins(size=30)

    background.rectangle((20, 20), 894, 242, "#2a2e35")
    background.paste(profile, (50, 50))
    background.ellipse(
        (42, 42), width=206, height=206, outline="#43b581", stroke_width=10
    )
    background.rectangle(
        (260, 180), width=630, height=40, fill="#484b4e", radius=20
    )
    background.bar(
        (260, 180),
        max_width=630,
        height=40,
        percentage=percentage,
        fill="#00fa81",
        radius=20,
    )
    background.text((270, 120), name, font=poppins, color="#00fa81")
    background.text(
        (870, 125),
        f"{xp} / {next_level_xp}",
        font=poppins,
        color="#00fa81",
        align="right",
    )

    rank_level_texts = [
        Text("Classement ", color="#00fa81", font=poppins),
        Text(f"{rank}", color="#1EAAFF", font=poppins),
        Text("   Niveau ", color="#00fa81", font=poppins),
        Text(f"{level}", color="#1EAAFF", font=poppins),
    ]

    background.multi_text((850, 30), texts=rank_level_texts, align="right")

    output_path = os.path.join(output_dir, "profile_card.png")
    background.save(output_path)
    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
