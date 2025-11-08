
from flask import Flask, render_template, request, jsonify, send_file
from googletrans import Translator, LANGUAGES as GT_LANGUAGES
from gtts import gTTS
from gtts.lang import tts_langs
import io

app = Flask(__name__)

ALIASES = {
    "zh": "zh-cn",
    "zh-cn": "zh-cn",
    "zh_cn": "zh-cn",
    "chinese": "zh-cn",
    "chinese (simplified)": "zh-cn",
    "simplified chinese": "zh-cn",
    "zh-sg": "zh-cn",
    "zh-hans": "zh-cn",
    "zhcn": "zh-cn",
    "zh-hk": "zh-tw",
    "zh-tw": "zh-tw",
    "zh_tw": "zh-tw",
    "zh-hant": "zh-tw",
    "chinese (traditional)": "zh-tw",
    "traditional chinese": "zh-tw",
    "zhtw": "zh-tw",
}
for code, name in GT_LANGUAGES.items():
    ALIASES[code] = code
    ALIASES[code.lower()] = code
    ALIASES[code.upper()] = code
    ALIASES[name] = code
    ALIASES[name.lower()] = code
    ALIASES[name.title()] = code
    if "-" in code:
        ALIASES[code.replace("-", "_")] = code
        ALIASES[code.replace("-", "").lower()] = code
        ALIASES[code.replace("-", "").upper()] = code

def normalize(lang: str) -> str:
    if not lang:
        return "auto"
    key = lang.strip()
    return ALIASES.get(key, ALIASES.get(key.lower(), key.lower()))

GTTS_LANGS = tts_langs()
TTS_ALIASES = {
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh_cn": "zh-CN",
    "zh-hans": "zh-CN",
    "simplified chinese": "zh-CN",
    "chinese (simplified)": "zh-CN",
    "zh-tw": "zh-TW",
    "zh_tw": "zh-TW",
    "zh-hant": "zh-TW",
    "traditional chinese": "zh-TW",
    "chinese (traditional)": "zh-TW",
    "zh-hk": "zh-TW",
}
for code, name in GTTS_LANGS.items():
    TTS_ALIASES[code] = code
    TTS_ALIASES[code.lower()] = code
    TTS_ALIASES[code.upper()] = code
    TTS_ALIASES[name] = code
    TTS_ALIASES[name.lower()] = code
    TTS_ALIASES[name.title()] = code
    if "-" in code:
        TTS_ALIASES[code.replace("-", "_")] = code

def normalize_tts(lang: str) -> str:
    if not lang:
        return "en"
    key = lang.strip()
    return TTS_ALIASES.get(key, TTS_ALIASES.get(key.lower(), "en"))

@app.route("/")
def index():
    items = sorted([(code, name.title()) for code, name in GT_LANGUAGES.items()],
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

    if source not in GT_LANGUAGES and source != "auto":
        return jsonify({"ok": False, "error": f"Unsupported source language: {source}."}), 400
    if target not in GT_LANGUAGES:
        return jsonify({"ok": False, "error": f"Unsupported target language: {target}."}), 400

    try:
        translator = Translator()
        result = translator.translate(text, src=source, dest=target)
        return jsonify({
            "ok": True,
            "source": source,
            "target": target,
            "detected": getattr(result, "src", source),
            "translated_text": result.text
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
    return jsonify({code: name.title() for code, name in GT_LANGUAGES.items()})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
