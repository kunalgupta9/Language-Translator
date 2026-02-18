from flask import Flask, render_template, request, jsonify, send_file
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES as GT_LANGUAGES
from gtts import gTTS
from gtts.lang import tts_langs
import io

app = Flask(__name__)

ALIASES = {}
for name, code in GT_LANGUAGES.items():
    ALIASES[code] = code
    ALIASES[code.lower()] = code
    ALIASES[code.upper()] = code
    ALIASES[name] = code
    ALIASES[name.lower()] = code
    ALIASES[name.title()] = code

def normalize(lang: str) -> str:
    if not lang:
        return "auto"
    key = lang.strip()
    return ALIASES.get(key, ALIASES.get(key.lower(), key.lower()))

GTTS_LANGS = tts_langs()

TTS_ALIASES = {}
for code, name in GTTS_LANGS.items():
    TTS_ALIASES[code] = code
    TTS_ALIASES[code.lower()] = code
    TTS_ALIASES[code.upper()] = code
    TTS_ALIASES[name] = code
    TTS_ALIASES[name.lower()] = code
    TTS_ALIASES[name.title()] = code

def normalize_tts(lang: str) -> str:
    if not lang:
        return "en"
    key = lang.strip()
    return TTS_ALIASES.get(key, TTS_ALIASES.get(key.lower(), "en"))

@app.route("/")
def index():
    items = sorted([(code, name.title()) for name, code in GT_LANGUAGES.items()],
                   key=lambda x: x[1])
    return render_template("index.html", languages=items)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    source = normalize(data.get("source", "auto"))
    target = normalize(data.get("target", "en"))

    if not text:
        return jsonify({"ok": False, "error": "Please enter some text to translate."}), 400

    try:
        translated_text = GoogleTranslator(source=source, target=target).translate(text)
        return jsonify({
            "ok": True,
            "source": source,
            "target": target,
            "translated_text": translated_text
        })
    except Exception as e:
        return jsonify({"ok": False, "error": f"Translation failed: {e}"}), 500

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    lang = normalize_tts(data.get("lang", "en"))

    if not text:
        return jsonify({"ok": False, "error": "No text to speak."}), 400
    if lang not in GTTS_LANGS:
        return jsonify({"ok": False, "error": f"TTS not supported for language: {lang}"}), 400

    try:
        tts = gTTS(text=text, lang=lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return send_file(buf, mimetype="audio/mpeg", as_attachment=False, download_name="tts.mp3")
    except Exception as e:
        return jsonify({"ok": False, "error": f"TTS failed: {e}"}), 500

@app.route("/languages")
def languages():
    return jsonify({code: name.title() for name, code in GT_LANGUAGES.items()})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
