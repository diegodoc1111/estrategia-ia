# Arma docs/prompts/superheroe-prompts.txt a partir de los prompts reales del video (clon-blender-3), sin datos
# personales y sin la marca del murciélago (emblema genérico), y la miniatura docs/img/video-superheroe.jpg.
import os, re, subprocess
from PIL import Image
AQUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(AQUI, "..", "..", "Metodo-Escala", "Reels", "clon-blender-3")
G = os.path.join(P, "guias", "prompts")
lee = lambda n: open(os.path.join(G, n), encoding="utf-8").read().strip()

def limpia(s):
    rep = [("bat-themed ", ""),
           ("A large BLACK BAT EMBLEM with spread wings across the middle of the chest, raised in relief on a sculpted grey chest plate.",
            "A large BLACK EMBLEM of your own design ([YOUR EMBLEM]) across the middle of the chest, raised in relief on a sculpted grey chest plate."),
           ("a large BLACK BAT EMBLEM with spread wings across the chest", "a large BLACK EMBLEM ([YOUR EMBLEM]) across the chest"),
           ("NO cape, NO cowl, NO mask, NO ears, NO helmet", "NO cape, NO cowl, NO mask, NO helmet"),
           ("NO cape, NO cowl, NO mask, NO bat ears, NO helmet", "NO cape, NO cowl, NO mask, NO helmet"),
           ("No cape, no cowl, no mask, no bat ears, no helmet, no weapon.", "No cape, no cowl, no mask, no helmet, no weapon."),
           ("the top of the bat emblem", "the top of the emblem"), ("other than the bat emblem on the chest", "other than the emblem on the chest"),
           ("the bat emblem on his chest", "the emblem on his chest"),
           ("his BLACK RECTANGULAR GLASSES, which he wears in every panel; short dark hair; a trimmed dark beard;", "[YOUR LOOK: glasses or not, hair, beard];"),
           ("his exact face; BLACK RECTANGULAR GLASSES, always on; short dark hair; a trimmed dark beard;", "his exact face; [YOUR LOOK: glasses or not, hair, beard];"),
           ("with his black rectangular glasses, his trimmed beard and", "with"),
           ("his skin and his glasses are unmarked", "his skin is unmarked"),
           ("the glasses and the top", "the top"), ("eyes, glasses, beard, fabric", "eyes, fabric"),
           ("with his black rectangular glasses. No weapon.", "No weapon."),
           ("the same face, glasses, build and suit", "the same face, build and suit"),
           ("Take only his face, glasses, hair and identity", "Take only his face, hair and identity")]
    for a, b in rep:
        s = s.replace(a, b)
    return s

RAYA = "=" * 78
partes = ['PROMPTS QUE ESCRIBIÓ CLAUDE PARA "NUNCA SUBESTIMES AL DE LAS GAFAS" (@soydiegoosorio)',
          'CÓMO USARLOS: pégale este archivo a Claude Code (con Higgsfield conectado) y dile "haz este video con mi clon".',
          "Image 1 = tu ficha con el traje (Claude la crea con GPT Image 2.6) · Image 2 = una foto de tu cara.",
          "Seedance 2.5 en Higgsfield: 9:16, 480p, con audio, una generación por escena. Cambia [YOUR LOOK] por cómo eres tú",
          "y [YOUR EMBLEM] por el emblema de TU traje (invéntalo: no uses logos ni personajes de marcas).",
          "Video 1 = un bloqueo hecho en Blender con muñecos simples SIN brazos (dónde está cada uno, la cámara y los tiempos).",
          "Si no usas Blender, borra el párrafo que empieza por VIDEO 1 y quita «Video 1» de cada escena: funciona, pero la",
          "física sale menos exacta. Cada escena = BLOQUE BASE + su texto. Duraciones: 9, 5, 7, 4, 10, 4, 5 y 9 segundos.",
          "", RAYA, "FICHA DEL PERSONAJE (GPT Image 2.6, 16:9, con 3 fotos tuyas)", RAYA, "", limpia(lee("ficha_murcielago.txt")),
          "", RAYA, "BLOQUE BASE (va arriba de CADA escena)", RAYA, "", limpia(lee("base_sin_brazos.txt"))]
for n, (arch, tit) in enumerate((("e1_banco", "EL BANCO"), ("e2_camioneta", "LA CAMIONETA"), ("e3_futbol", "EL FÚTBOL"),
                                 ("e4_gimnasio", "EL GIMNASIO"), ("e5_lucha", "LA LUCHA LIBRE"), ("e6_trasteo", "EL TRASTEO"),
                                 ("e7_bus", "EL BUS"), ("e8_selfie", "LA SELFIE DEL CIERRE (encima va tu voz en off)")), 1):
    partes += ["", RAYA, f"ESCENA {n} · {tit}", RAYA, "", limpia(lee(arch + ".txt"))]
txt = "\n".join(partes) + "\n"
for malo in ("diego", "osorio", " bat ", "batman", "bat-", "murci"):
    resto = txt.lower().replace("@soydiegoosorio", "")
    assert malo not in resto, malo
os.makedirs(os.path.join(AQUI, "docs", "prompts"), exist_ok=True)
open(os.path.join(AQUI, "docs", "prompts", "superheroe-prompts.txt"), "w", encoding="utf-8").write(txt)
print("prompts", len(txt), "caracteres")
# miniatura 928x522 del cuadro donde sostiene al gigante
tmp = os.path.join(AQUI, "_cuadro.png")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "28.6", "-i", os.path.join(P, "Nunca subestimes al de las gafas - FINAL.mp4"),
                "-frames:v", "1", tmp], check=True)
im = Image.open(tmp).convert("RGB")
y0 = 560
im.crop((0, y0, 1080, y0 + 608)).resize((928, 522), Image.LANCZOS).save(os.path.join(AQUI, "docs", "img", "video-superheroe.jpg"), quality=88)
os.remove(tmp)
print("miniatura ok")
