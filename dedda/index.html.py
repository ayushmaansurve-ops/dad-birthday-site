#!/usr/bin/env python3
"""
Birthday Website Generator - Happy Birthday Dedda!

HOW TO USE IN PYCHARM:
  1. Put all your photos in a folder called  'photos'  next to this script
  2. Name them exactly as listed in MEMORIES below
  3. Press Shift+F10 to run
  4. birthday_dedda.html opens in your browser automatically

Required:  pip install Pillow
"""

import os
import base64
import webbrowser
from io import BytesIO

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Note: Pillow not installed. Photos will be embedded at full size.")
    print("To install: pip install Pillow")


# ── Photo filenames & captions ────────────────────────────────────────────────
MEMORIES = [
    ("1000026137.jpg", "The Man in the Room",
     "There was always something about the way you carried yourself — relaxed, warm, "
     "completely at ease. A quiet confidence that made every room feel lighter."),

    ("1000026121.jpg", "Ready for the World",
     "Backpack on, eyes forward. You always moved like someone who knew exactly where "
     "you were going — and somehow, you always got there."),

    ("1000026127.jpg", "The Patriot",
     "You wore your roots proudly — on your head, on your face, in your heart. "
     "You never forgot where you came from, and that made all of us proud too."),

    ("1000026109.jpg", "A Quiet Morning",
     "Even in the simplest moments — a coffee, a glass of juice — you had a way of "
     "making everything feel like it mattered. Those mornings were everything."),

    ("1000026102.jpg", "Your Own Man",
     "You never tried to be anything other than yourself. Unbothered, steady, real. "
     "That is a kind of strength most people spend their whole lives searching for."),

    ("1000026135.jpg", "Dubai Days",
     "You built a life in a city that never sleeps. Far from home, you made it yours — "
     "and in doing so, you made it ours too. Every sacrifice was for us."),

    ("1000026118.jpg", "The Wanderer",
     "Standing at the edge of the world, the sea stretching out behind you. "
     "You always had that look — like you could see something in the distance the rest of us could not yet."),

    ("1000026139.jpg", "Together Always",
     "Side by side through every landscape. The family you built is the greatest journey "
     "you ever took. And you never had to travel it alone."),

    ("1000026130.jpg", "The Love That Started It All",
     "This smile. This moment. This is where the whole story begins. "
     "Everything we are grew from the love in this photograph."),

    ("1000026093.jpg", "Day One",
     "The moment a father is born. That smile — pure, wide, completely unguarded — "
     "is one of the most beautiful things we have ever seen."),

    ("1000026112.jpg", "The Gentle Nights",
     "Late nights, tiny hands, the weight of someone who trusted you completely. "
     "You never once made it feel like a burden. That is what love looks like."),

    ("1000026124.jpg", "His Superman",
     "He wore that shirt, but we all know — "
     "you were always the real Superman. You still are."),

    ("1000026115.jpg", "Joy is Contagious",
     "That laugh. Open-mouthed, eyes squinting, completely free. "
     "It has been the soundtrack of our happiest moments. Long may it ring."),

    ("1000026133.jpg", "A Million Little Moments",
     "Christmas mornings, silly selfies, sleepy cuddles. These are the moments "
     "that make a childhood. You gave all of them, every single one."),

    ("1000026142.jpg", "Father and Son",
     "Two generations, and the resemblance is not just in the face. It is in the eyes, "
     "the posture, the quiet dignity. You are his hero, as you are ours."),
]

TODAY_PHOTO = "WIN_20250926_20_32_24_Pro.jpg"

PHOTOS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")


# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --cream: #fdf8f2; --warm: #fff9f3;
  --amber: #c47d2e; --ambers: #e8a55a; --gold: #d4962a;
  --dk: #3d1f07; --tx: #4a2c10; --soft: #7a5533; --lt: #a07850;
  --sh: 0 6px 40px rgba(100,60,20,.10);
}
html { scroll-behavior: smooth; }
body {
  background: var(--cream); color: var(--tx);
  font-family: 'Nunito', sans-serif; font-weight: 300;
  line-height: 1.75; overflow-x: hidden;
}
.hero {
  min-height: 100vh;
  background: linear-gradient(150deg, #fef4e4, #fdebd0 45%, #f8dfc0);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center; padding: 80px 24px 120px;
  position: relative; overflow: hidden;
}
.orb { position: absolute; border-radius: 50%; pointer-events: none; }
.o1 {
  width: 700px; height: 700px;
  background: radial-gradient(circle, rgba(212,150,42,.13), transparent 65%);
  top: -200px; right: -150px;
}
.o2 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(196,125,46,.10), transparent 65%);
  bottom: -150px; left: -100px;
}
.htag {
  font-size: .7rem; letter-spacing: .42em; text-transform: uppercase;
  color: var(--amber); font-weight: 600; margin-bottom: 22px;
  animation: fu 1s ease both;
}
.htitle {
  font-family: 'Playfair Display', serif;
  font-size: clamp(3rem, 9vw, 6.5rem);
  font-weight: 700; color: var(--dk);
  line-height: 1.08; margin-bottom: 18px;
  animation: fu 1s .18s ease both;
}
.hrt { color: #c0392b; }
.rule {
  width: 72px; height: 1.5px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  margin: 22px auto; animation: fu 1s .3s ease both;
}
.hsub {
  font-family: 'Playfair Display', serif; font-style: italic;
  font-size: clamp(1.1rem, 3vw, 1.55rem);
  color: var(--soft); animation: fu 1s .38s ease both;
}
.scue {
  position: absolute; bottom: 38px; left: 50%; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; gap: 9px;
  color: var(--lt); font-size: .68rem; letter-spacing: .28em;
  text-transform: uppercase; animation: fu 1s .8s ease both;
}
.arr {
  width: 18px; height: 18px;
  border-right: 1.5px solid var(--ambers);
  border-bottom: 1.5px solid var(--ambers);
  transform: rotate(45deg); animation: ab 2.2s infinite;
}
.tl {
  max-width: 680px; margin: 0 auto;
  padding: 90px 20px 60px; position: relative;
}
.tl::before {
  content: ''; position: absolute;
  left: 50%; top: 90px; bottom: 60px; width: 1px;
  background: linear-gradient(to bottom, transparent, var(--ambers) 8%, var(--ambers) 92%, transparent);
  transform: translateX(-50%);
}
@media (max-width: 560px) { .tl::before { left: 28px; transform: none; } }
.card {
  background: var(--warm); border-radius: 22px;
  box-shadow: var(--sh); overflow: hidden; margin-bottom: 72px;
  position: relative; opacity: 0; transform: translateY(44px);
  transition: opacity .75s cubic-bezier(.22,.68,0,1.2),
              transform .75s cubic-bezier(.22,.68,0,1.2);
}
.card.vis { opacity: 1; transform: translateY(0); }
.ca {
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--amber), var(--gold), var(--ambers));
}
.ci { width: 100%; height: auto; display: block; }
.cb { padding: 26px 30px 30px; }
.cl {
  font-size: .65rem; letter-spacing: .38em; text-transform: uppercase;
  font-weight: 600; color: var(--amber); margin-bottom: 10px;
}
.cm {
  font-family: 'Playfair Display', serif; font-style: italic;
  font-size: clamp(1rem, 2.4vw, 1.18rem);
  color: var(--tx); line-height: 1.85;
}
.fin {
  background: linear-gradient(140deg, #2e1204, #5c2d0e, #3d1a05);
  border-radius: 26px; padding: 60px 40px;
  text-align: center; margin: 0 0 100px;
  position: relative; overflow: hidden;
  opacity: 0; transform: translateY(44px);
  transition: opacity .85s ease, transform .85s ease;
}
.fin.vis { opacity: 1; transform: translateY(0); }
.fg { position: absolute; border-radius: 50%; pointer-events: none; }
.fg1 {
  width: 450px; height: 450px;
  background: radial-gradient(circle, rgba(212,150,42,.18), transparent 65%);
  top: -120px; right: -100px;
}
.fg2 {
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(196,125,46,.12), transparent 65%);
  bottom: -80px; left: -60px;
}
.ftodayimg {
  width: 100%; height: auto; display: block;
  border-radius: 16px; margin-bottom: 32px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.ftag {
  font-size: .68rem; letter-spacing: .42em; text-transform: uppercase;
  color: var(--gold); font-weight: 600; margin-bottom: 22px;
}
.ftitle {
  font-family: 'Playfair Display', serif; font-weight: 700;
  font-size: clamp(1.9rem, 5vw, 3.1rem);
  color: #fff; line-height: 1.18; margin-bottom: 28px;
}
.frule { width: 52px; height: 1.5px; background: var(--gold); margin: 0 auto 28px; }
.fmsg {
  font-family: 'Playfair Display', serif; font-style: italic;
  font-size: clamp(1.05rem, 2.5vw, 1.22rem);
  color: rgba(255,255,255,.83); line-height: 1.95;
  max-width: 500px; margin: 0 auto 36px;
}
.fsig { font-size: .82rem; letter-spacing: .18em; color: var(--gold); }
@keyframes fu {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes ab {
  0%, 100% { transform: rotate(45deg) translate(0, 0); }
  50%       { transform: rotate(45deg) translate(4px, 4px); }
}
@media (max-width: 560px) {
  .cb  { padding: 18px 18px 22px; }
  .fin { padding: 40px 22px; }
}
"""

JS = """
const io = new IntersectionObserver(
  e => e.forEach(x => { if (x.isIntersecting) x.target.classList.add('vis'); }),
  { threshold: 0.10 }
);
document.querySelectorAll('.card, .fin').forEach(el => io.observe(el));
"""


# ── Helpers ───────────────────────────────────────────────────────────────────
def photo_to_base64(filename):
    """Load a photo from the photos folder and return a base64 string."""
    path = os.path.join(PHOTOS_FOLDER, filename)
    if not os.path.exists(path):
        print(f"  WARNING: Photo not found: {path}")
        return None

    if PIL_AVAILABLE:
        img = Image.open(path)
        img.thumbnail((800, 900), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=78)
        return base64.b64encode(buf.getvalue()).decode()
    else:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()


# ── HTML builder ──────────────────────────────────────────────────────────────
def build_html():
    gf = ("https://fonts.googleapis.com/css2?family=Playfair+Display:"
          "ital,wght@0,500;0,700;1,400&family=Nunito:wght@300;400;600&display=swap")

    parts = [f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Happy Birthday Dedda &#10084;&#65039;</title>
  <link href="{gf}" rel="stylesheet"/>
  <style>{CSS}</style>
</head>
<body>

<section class="hero">
  <div class="orb o1"></div>
  <div class="orb o2"></div>
  <p class="htag">For the man who gave us everything</p>
  <h1 class="htitle">Happy Birthday<br>Dedda <span class="hrt">&#10084;&#65039;</span></h1>
  <div class="rule"></div>
  <p class="hsub">15 Moments. A Lifetime of Memories.</p>
  <div class="scue"><span>Scroll</span><div class="arr"></div></div>
</section>

<main class="tl">
"""]

    # Memory cards
    print("Embedding photos...")
    for fname, label, quote in MEMORIES:
        print(f"  {fname}...")
        b64 = photo_to_base64(fname)
        if b64:
            img_tag = f'<img class="ci" src="data:image/jpeg;base64,{b64}" alt="{label}"/>'
        else:
            img_tag = f'<div style="background:#f0e6d8;height:200px;display:flex;align-items:center;justify-content:center;color:#a07850">Photo not found: {fname}</div>'

        parts.append(f"""<article class="card">
  <div class="ca"></div>
  {img_tag}
  <div class="cb">
    <p class="cl">{label}</p>
    <p class="cm">{quote}</p>
  </div>
</article>
""")

    # Final birthday card
    print(f"  {TODAY_PHOTO} (today)...")
    today_b64 = photo_to_base64(TODAY_PHOTO)
    today_tag = (
        f'<img class="ftodayimg" src="data:image/jpeg;base64,{today_b64}" alt="Today"/>'
        if today_b64 else ""
    )

    parts.append(f"""<div class="fin">
  <div class="fg fg1"></div>
  <div class="fg fg2"></div>
  {today_tag}
  <p class="ftag">Today &middot; Your Birthday</p>
  <h2 class="ftitle">To the man who<br>built us all</h2>
  <div class="frule"></div>
  <p class="fmsg">
    There are no words big enough for what you mean to us.<br/><br/>
    You gave up so much, so quietly, without ever asking for anything in return.
    You loved without conditions. You showed up, every single time.
    You made us feel safe in a world that is not always gentle.<br/><br/>
    Today is about you. All of you. The young man in every old photograph.
    The father in every tender moment. The man standing right here, right now
    &mdash; who we are so endlessly proud to call ours.<br/><br/>
    Happy Birthday, Dedda. We love you more than we will ever know how to say.
  </p>
  <div class="frule"></div>
  <p class="fsig">&#8212; Loved by Ayushmaan &#10084;&#65039;</p>
</div>
</main>
<script>{JS}</script>
</body>
</html>
""")

    return "".join(parts)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Birthday Website Generator")
    print("  Happy Birthday Dedda! ❤️")
    print("=" * 50)

    # Check photos folder exists
    if not os.path.exists(PHOTOS_FOLDER):
        os.makedirs(PHOTOS_FOLDER)
        print(f"\nCreated folder: {PHOTOS_FOLDER}")
        print("Please copy all your photos into this folder, then run again.")
        return

    html = build_html()

    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "birthday_dedda.html")
    with open(output, "w", encoding="utf-8") as fh:
        fh.write(html)

    size_kb = os.path.getsize(output) // 1024
    print(f"\nDone! File saved: {output}")
    print(f"Size: {size_kb} KB")
    print("Opening in your browser...")
    webbrowser.open(f"file://{output}")


if __name__ == "__main__":
    main()
