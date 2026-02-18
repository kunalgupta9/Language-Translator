
let controller = null;

function debounce(fn, delay = 400) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), delay);
  };
}

async function doTranslate() {
  const text = document.getElementById("input").value.trim();
  const source = document.getElementById("source").value;
  const target = document.getElementById("target").value;
  const errorBox = document.getElementById("error");
  const out = document.getElementById("output");
 const speakBtn = document.getElementById("speak");
const autospeak = document.getElementById("autospeak");


  errorBox.style.display = "none";

  if (!text) {
    out.value = "";
    speakBtn.disabled = true;
    player.style.display = "none";
    return;
  }

  if (controller) controller.abort();
  controller = new AbortController();
  out.placeholder = "Translating…";

  try {
    const res = await fetch("/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, source, target }),
      signal: controller.signal,
    });
    const data = await res.json();
    if (!data.ok) {
      errorBox.innerText = data.error || "Unknown error.";
      errorBox.style.display = "block";
      out.placeholder = "Translation will appear here...";
      speakBtn.disabled = true;
      return;
    }
    out.value = data.translated_text;
    speakBtn.disabled = false;

    if (autospeak.checked) {
      await speak();
    }
  } catch (e) {
    if (e.name !== "AbortError") {
      errorBox.innerText = "Network or server error: " + e;
      errorBox.style.display = "block";
    }
  } finally {
    out.placeholder = "Translation will appear here...";
  }
}

async function speak() {
  const text = document.getElementById("output").value.trim();
  const lang = document.getElementById("target").value;
  const errorBox = document.getElementById("error");
  const player = document.getElementById("player");

  if (!text) return;

  try {
    const res = await fetch("/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, lang }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      errorBox.innerText = (err && err.error) ? err.error : "TTS error.";
      errorBox.style.display = "block";
      return;
    }
    const blob = await res.blob();
const url = URL.createObjectURL(blob);
const audio = new Audio(url);   
audio.play();                  

  } catch (e) {
    errorBox.innerText = "Audio error: " + e;
    errorBox.style.display = "block";
  }
}

document.getElementById("translate").addEventListener("click", doTranslate);
document.getElementById("speak").addEventListener("click", speak);

const debounced = debounce(doTranslate, 400);
document.getElementById("input").addEventListener("input", debounced);
document.getElementById("source").addEventListener("change", doTranslate);
document.getElementById("target").addEventListener("change", doTranslate);
document.getElementById("swap").addEventListener("click", () => {
  const s = document.getElementById("source");
  const t = document.getElementById("target");
  const tmp = s.value;
  s.value = t.value;
  t.value = tmp;
  doTranslate();
});
