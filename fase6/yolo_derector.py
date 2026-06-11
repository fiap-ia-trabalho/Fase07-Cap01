import io
from pathlib import Path
from typing import Any, BinaryIO, Union

import numpy as np
import torch
from PIL import Image

FASE6_DIR = Path(__file__).parent
YOLO_DIR = FASE6_DIR / "yolov5"
MODEL_PATH = FASE6_DIR / "best.pt"
TEST_DIR = FASE6_DIR / "test"
CLASSES_PRAGA = {"diseased", "Planta doente"}

_model = None


def _carregar_modelo():
    global _model
    if _model is None:
        _model = torch.hub.load(
            str(YOLO_DIR),
            "custom",
            path=str(MODEL_PATH),
            source="local",
            force_reload=False,
        )
        _model.conf = 0.25
        _model.iou = 0.45
    return _model


def _preparar_imagem(imagem: Union[str, Path, bytes, np.ndarray, Image.Image, BinaryIO]) -> Any:
    """Converte a entrada do dashboard (arquivo, bytes ou PIL) para o formato aceito pelo YOLO."""
    if isinstance(imagem, (str, Path)):
        caminho = Path(imagem)
        if caminho.is_dir():
            raise IsADirectoryError(f"Envie um arquivo de imagem, não uma pasta: {caminho}")
        return np.array(Image.open(caminho).convert("RGB"))

    if isinstance(imagem, bytes):
        return np.array(Image.open(io.BytesIO(imagem)).convert("RGB"))

    if isinstance(imagem, Image.Image):
        return np.array(imagem.convert("RGB"))

    if isinstance(imagem, np.ndarray):
        return imagem

    if hasattr(imagem, "read"):
        imagem.seek(0)
        return np.array(Image.open(imagem).convert("RGB"))

    raise TypeError(
        "Formato de imagem não suportado. Use caminho, bytes, PIL.Image, numpy.ndarray "
        "ou arquivo enviado pelo Streamlit."
    )


def detectar_imagem(imagem: Union[str, Path, bytes, np.ndarray, Image.Image, BinaryIO]) -> dict:
    """
    Recebe uma imagem vinda do dashboard e retorna o resultado da detecção.

    Retorno:
        {
            "praga_detectada": bool,
            "total_deteccoes": int,
            "deteccoes": [{"classe": str, "confianca": float, "bbox": [x1, y1, x2, y2]}, ...],
            "imagem_anotada": bytes  # PNG com as caixas desenhadas
        }
    """
    model = _carregar_modelo()
    img = _preparar_imagem(imagem)
    results = model(img)

    deteccoes = []
    praga_detectada = False

    df = results.pandas().xyxy[0]
    for _, row in df.iterrows():
        classe = row["name"]
        confianca = round(float(row["confidence"]), 4)
        bbox = [
            round(float(row["xmin"]), 2),
            round(float(row["ymin"]), 2),
            round(float(row["xmax"]), 2),
            round(float(row["ymax"]), 2),
        ]
        deteccoes.append({
            "classe": classe,
            "confianca": confianca,
            "bbox": bbox,
        })
        if classe in CLASSES_PRAGA or "doente" in classe.lower():
            praga_detectada = True

    results.render()
    img_anotada = Image.fromarray(results.ims[0])
    buffer = io.BytesIO()
    img_anotada.save(buffer, format="PNG")

    return {
        "praga_detectada": praga_detectada,
        "total_deteccoes": len(deteccoes),
        "deteccoes": deteccoes,
        "imagem_anotada": buffer.getvalue(),
    }


if __name__ == "__main__":
    output_dir = FASE6_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    imagens = sorted(TEST_DIR.glob("*.jpg")) + sorted(TEST_DIR.glob("*.png"))
    if not imagens:
        raise FileNotFoundError(f"Nenhuma imagem encontrada em {TEST_DIR}")

    for caminho in imagens:
        resultado = detectar_imagem(caminho)
        print(f"\n--- {caminho.name} ---")
        print("Praga detectada:", resultado["praga_detectada"])
        print("Detecções:", resultado["deteccoes"])

        saida = output_dir / f"resultado_{caminho.stem}.png"
        saida.write_bytes(resultado["imagem_anotada"])
        print(f"Imagem salva em: {saida}")
