import PyPDF2
from setup_logging import logger 

def read_pdf_file(file_path):

    text = ""
    
    try:
        logger.info(f"Попытка чтения файла: {file_path}")
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        logger.info(f"✅ Успешно прочитано {len(pdf_reader.pages)} страниц.")
        return text
    
    except FileNotFoundError as e:
        logger.error(f"🚫 Файл не найден: {e}")
        return None
    except PyPDF2.PdfReadError as e:
        logger.error(f"⭕️ Ошибка чтения PDF: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Неизвестная ошибка: {e}", exc_info=True)  # exc_info=True для traceback
        return None

if __name__ == "__main__":
    file_path = "input\example.pdf"
    
    extracted_text = read_pdf_file(file_path)