from openai import OpenAI
import yaml
from pathlib import Path
from typing import List, Dict
import asyncio
import time

class DataMiner:
    def __init__(self):
        self.config = self._load_config()
        self.client = self._setup_client()
    
    def _load_config(self) -> Dict:
        config_path = Path(__file__).parent.parent / "config" / "ai_config.yaml"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)["data_miner"]
        except Exception as e:
            raise Exception(f"Ошибка загрузки конфига: {str(e)}")
    
    def _setup_client(self):
        return OpenAI(
            base_url=self.config["api_base"],
            api_key=self.config["api_key"]
        )
    
    async def analyze_chunk(self, chunk: str) -> str:
        try:
            completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": self.config["system_prompt"]},
                    {"role": "user", "content": chunk}
                ],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"]
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")
    
    async def process_document(self, chunks: List[str]) -> List[str]:
        return await asyncio.gather(*[self.analyze_chunk(chunk) for chunk in chunks])
    
    async def process_document_raw(self, chunks: List[str]) -> dict:
        responses = []
        for chunk in chunks:
            response = await self._make_api_request(chunk)
            responses.append(response)
    
        return {
            "model": self.config["model"],
            "timestamp": time.now().isoformat(),
            "responses": responses
        }

    async def _make_api_request(self, chunk: str) -> dict:
        completion = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.config["model"],
            messages=[
                {"role": "system", "content": self.config["system_prompt"]},
                {"role": "user", "content": chunk}
            ],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"]
        )
        return completion.to_dict()