"""
TopMelhoresPromo — Redimensionador de Imagens v2
=================================================
Redimensiona para 400x400px SEM CORTAR a imagem.
A imagem é centralizada com fundo BRANCO preenchendo as bordas.
Ideal para fotos de produtos.

COMO USAR:
1. pip install Pillow
2. Coloque este script dentro da pasta 'images/'
3. python redimensionar.py
"""

import os
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("❌ Pillow não instalado. Execute: pip install Pillow")
    exit(1)

TAMANHO      = (400, 400)
QUALIDADE    = 88
COR_FUNDO    = (255, 255, 255)   # branco
PASTA        = Path(__file__).parent
PASTA_BACKUP = PASTA / "originais"

def redimensionar(caminho: Path) -> bool:
    try:
        with Image.open(caminho) as img:
            if img.mode in ("RGBA", "P", "LA", "L"):
                img = img.convert("RGB")

            # Redimensiona mantendo proporção SEM cortar
            img.thumbnail(TAMANHO, Image.LANCZOS)

            # Cria canvas branco 400x400 e centraliza a imagem
            canvas = Image.new("RGB", TAMANHO, COR_FUNDO)
            x = (TAMANHO[0] - img.width)  // 2
            y = (TAMANHO[1] - img.height) // 2
            canvas.paste(img, (x, y))

            destino = caminho.with_suffix(".jpg")
            canvas.save(str(destino), "JPEG", quality=QUALIDADE, optimize=True)

            if caminho.suffix.lower() in (".png", ".webp") and destino != caminho:
                caminho.unlink()

        return True
    except Exception as e:
        print(f"   ⚠️  Erro: {caminho.name} — {e}")
        return False


def main():
    print("=" * 50)
    print("  TopMelhoresPromo — Redimensionador v2")
    print("  Modo: centralizado com fundo branco")
    print("=" * 50)

    imagens = [
        f for f in PASTA.iterdir()
        if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]

    if not imagens:
        print("\n⚠️  Nenhuma imagem encontrada.")
        return

    print(f"\n📁 {len(imagens)} imagem(ns) encontrada(s)")

    # Restaura originais do backup se existir
    if PASTA_BACKUP.exists():
        originais = list(PASTA_BACKUP.glob("*"))
        if originais:
            print(f"♻️  Restaurando {len(originais)} original(is) antes de reprocessar...")
            for orig in originais:
                shutil.copy2(orig, PASTA / orig.name)
            imagens = [
                f for f in PASTA.iterdir()
                if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
            ]

    # Backup
    PASTA_BACKUP.mkdir(exist_ok=True)
    for img in imagens:
        shutil.copy2(img, PASTA_BACKUP / img.name)
    print(f"💾 Backup salvo em: originais/")

    print(f"\n🔄 Redimensionando para 400x400px com fundo branco...\n")
    ok = erro = 0
    for img in sorted(imagens):
        if redimensionar(img):
            ok += 1
            print(f"   ✅  {img.name}")
        else:
            erro += 1

    print("\n" + "=" * 50)
    print(f"  ✅  {ok} processada(s) com sucesso")
    if erro:
        print(f"  ❌  {erro} com erro")
    print(f"  📐  400x400px | Fundo branco")
    print(f"  💾  Originais em: images/originais/")
    print("=" * 50)


if __name__ == "__main__":
    main()
