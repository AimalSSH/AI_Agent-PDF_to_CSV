from typing import Optional, List
from core.chunkers.pdf_chunker import PDFChunker
from services.logging_service import logger
import aiofiles
from PyPDF2 import PdfReader
import asyncio

class AsyncPDFProcessor:
    def __init__(self):
        self.chunker = PDFChunker()
    
    async def extract_text(self, file_path: str) -> Optional[str]:
        try:
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
                
                from io import BytesIO
                pdf_file = BytesIO(content)
                
                pdf = PdfReader(pdf_file)
                return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
                
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return None
    
    async def process_pdf(self, file_path: str) -> List[str]:
        text = await self.extract_text(file_path)
        return self.chunker.smart_chunking(text)