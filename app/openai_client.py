# app/openai_client.py

import os
from typing import Tuple

async def solve_text(content: str) -> Tuple[str, str]:
    """
    Простая «заглушка» для локального тестирования.
    Всегда возвращает текст «Решение задачи: {content}»
    и фиксированную SVG-строку.
    """
    return (
        f"Решение задачи: {content}",
        "<svg><!-- пример графики --></svg>"
    )

async def solve_image(path: str) -> Tuple[str, str]:
    """
    Заглушка для обработки изображения:
    возвращает имя файла и ту же фиктивную SVG-графику.
    """
    filename = os.path.basename(path)
    return (
        f"Решение по изображению: {filename}",
        "<svg><!-- пример графики --></svg>"
    )
