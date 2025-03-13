import google.generativeai as genai
from abc import ABC, abstractmethod
from typing import Optional
import asyncio
from functools import partial

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str, model_name: str = "gemini-pro", system_instruction: Optional[str] = None):
        self.model_name = model_name
        self.system_instruction = system_instruction
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    async def generate(self, prompt: str) -> str:
        try:
            # Combine system instruction with prompt if provided
            full_prompt = f"{self.system_instruction}\n\n{prompt}" if self.system_instruction else prompt
            
            # Run the synchronous generate_content in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(full_prompt).text
            )
            
            return response
        except Exception as e:
            print(f"Error in Gemini generation: {e}")
            raise