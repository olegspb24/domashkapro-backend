# app/core/ai_provider.py
from abc import ABC, abstractmethod
from app.core.config import settings
from app.openai_client import solve_text as openai_solve_text, solve_image as openai_solve_image

class AIClient(ABC):
    @abstractmethod
    async def solve_text(self, prompt: str) -> tuple[str, str]:
        ...

    @abstractmethod
    async def solve_image(self, image_path: str) -> tuple[str, str]:
        ...

class OpenAIClient(AIClient):
    async def solve_text(self, prompt: str) -> tuple[str, str]:
        return await openai_solve_text(prompt)

    async def solve_image(self, image_path: str) -> tuple[str, str]:
        return await openai_solve_image(image_path)

class DummyClient(AIClient):
    async def solve_text(self, prompt: str) -> tuple[str, str]:
        # Заглушка для второго провайдера
        return (f"[Dummy] Ответ на текст: {prompt}", "<svg><!-- dummy графика --></svg>")

    async def solve_image(self, image_path: str) -> tuple[str, str]:
        return (f"[Dummy] Ответ на изображение: {image_path}", "<svg><!-- dummy графика --></svg>")

# Фабрика клиента
def get_ai_client() -> AIClient:
    provider = settings.ai_provider or 'openai'
    if provider == 'dummy':
        return DummyClient()
    # default OpenAI
    return OpenAIClient()
