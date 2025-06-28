import asyncio
import json
import csv
import hashlib
from pathlib import Path
from datetime import datetime
from core.agents.data_miner import DataMiner
from services.pdf_service import AsyncPDFProcessor
from services.logging_service import logger

def save_unique_results(results: list, output_file: str = "output/raw_results.json"):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    existing_data = []
    if output_path.exists():
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
    
    existing_hashes = {entry.get('hash') for entry in existing_data if 'hash' in entry}
    
    new_entries = []
    for result in results:
        content_hash = hashlib.sha256(str(result).encode('utf-8')).hexdigest()
        
        if content_hash not in existing_hashes:
            new_entry = {
                'content': result,
                'hash': content_hash,
                'timestamp': datetime.now().isoformat(),
                'length': len(result)
            }
            new_entries.append(new_entry)
    
    if new_entries:
        all_data = existing_data + new_entries
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nСохранено {len(new_entries)} сырых результатов в {output_path}")
        return output_path
    
    print("\nНет новых сырых данных для сохранения")
    return None

def validate_and_convert(raw_file: Path):
    validated_dir = Path("output/validated")
    quarantine_dir = Path("quarantine")
    csv_dir = Path("output/csv")
    
    validated_dir.mkdir(parents=True, exist_ok=True)
    quarantine_dir.mkdir(exist_ok=True)
    csv_dir.mkdir(exist_ok=True)
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    valid_entries = []
    invalid_entries = []
    seen_hashes = set()
    
    for entry in raw_data:
        content = entry['content']
        clean_content = content.replace('```json\n', '').replace('```', '').strip()
        
        try:
            json_data = json.loads(clean_content)
            normalized_data = {
                'БИК': json_data.get('БИК', json_data.get('бИК', '')),
                'Название организации': json_data.get('Название организации', ''),
                'ОГРН': json_data.get('ОГРН', ''),
                'Телефон': json_data.get('Телефон', ''),
                'Электронная почта': json_data.get('Электронная почта', '')
            }
            
            if any(normalized_data.values()):
                data_hash = hashlib.sha256(
                    json.dumps(normalized_data, sort_keys=True).encode('utf-8')
                ).hexdigest()
                
                if data_hash not in seen_hashes:
                    seen_hashes.add(data_hash)
                    valid_entries.append(normalized_data)
        except json.JSONDecodeError:
            invalid_entries.append(entry)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stats = {'valid': len(valid_entries), 'invalid': len(invalid_entries)}
    
    if valid_entries:
        non_empty_entries = [row for row in valid_entries if any(row.values())]
        
        csv_file = csv_dir / f"result_{timestamp}.csv"
        fieldnames = ['БИК', 'Название организации', 'ОГРН', 'Телефон', 'Электронная почта']
        
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(non_empty_entries)
        
        print(f"\nCSV файл сохранен: {csv_file}")
    
    if invalid_entries:
        quarantine_file = quarantine_dir / f"invalid_{timestamp}.json"
        with open(quarantine_file, 'w', encoding='utf-8') as f:
            json.dump(invalid_entries, f, ensure_ascii=False, indent=2)
        print(f"\nНевалидные записи сохранены в: {quarantine_file}")
    
    return stats

async def process_document(file_path: str):
    try:
        pdf_processor = AsyncPDFProcessor()
        data_miner = DataMiner()
        
        logger.info(f"Начало обработки файла: {file_path}")
        print(f"\nОбработка файла: {file_path}")
        
        chunks = await pdf_processor.process_pdf(file_path)
        if not chunks:
            print("Не удалось извлечь текст из PDF")
            return
        
        print(f"Извлечено {len(chunks)} текстовых фрагментов")
        print("Анализ с помощью AI...")
        
        results = await data_miner.process_document(chunks)
        
        if results:
            raw_file = save_unique_results(results)
            
            if raw_file:
                stats = validate_and_convert(raw_file)
                print(f"\nСтатистика обработки:")
                print(f"- Валидных записей: {stats['valid']}")
                print(f"- Невалидных записей: {stats['invalid']}")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        print(f"\nКритическая ошибка: {e}")

if __name__ == "__main__":
    test_pdf = Path("data") / "example.pdf"
    
    if not test_pdf.exists():
        print(f"\nФайл {test_pdf} не найден!")
        print("Создайте папку 'data' и поместите туда PDF-файл с именем 'example.pdf'")
    else:
        asyncio.run(process_document(str(test_pdf)))