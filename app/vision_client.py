# app/vision_client.py

"""
Модуль работы с Vision API (заглушка).

Замените реализацию analyze_image на вызов реального сервиса,
когда он будет готов.
"""

async def analyze_image(image_url: str, question: str) -> str:
    """
    Пока без реального OpenAI-Vision.
    Возвращаем заглушку, чтобы убедиться, что всё работает.

    :param image_url: URL изображения для анализа
    :param question:  Текстовый вопрос к изображению
    :return:         Строка-ответ от «виртуального» Vision
    """
    return f"[DEMO-Vision] Я вижу файл {image_url}. Вопрос: {question}"


# Для обратной совместимости (если где-то вызывается ask_vision)
ask_vision = analyze_image
