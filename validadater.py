import json
import os
from pathlib import Path
from datetime import datetime
import hashlib

def clean_json_content(content: str):
    return content.replace('```json\n', '').replace('```', '').strip()

def validate_json_content(content: str):
    try:
        cleaned_content = clean_json_content(content)
        return json.loads(cleaned_content)
    except json.JSONDecodeError:
        return None

def process_raw_data(input_file: str = "output/results.json"):
    output_dir = Path("output/validated")
    quarantine_dir = Path("quarantine")
    output_dir.mkdir(parents=True, exist_ok=True)
    quarantine_dir.mkdir(exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    valid_entries = []
    invalid_entries = []
    seen_content_hashes = set()
    
    for entry in data:
        content = entry['content']
        json_data = validate_json_content(content)
        
        if json_data is None:
            invalid_entries.append(entry)
            continue
            
        content_hash = hashlib.sha256(
            json.dumps(json_data, sort_keys=True).encode('utf-8')
        ).hexdigest()
        
        if content_hash not in seen_content_hashes:
            seen_content_hashes.add(content_hash)
            valid_entries.append(json_data)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if valid_entries:
        output_file = output_dir / f"validated_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(valid_entries, f, ensure_ascii=False, indent=2)
        print(f"Сохранено {len(valid_entries)} уникальных валидных записей в {output_file}")
    
    if invalid_entries:
        quarantine_file = quarantine_dir / f"invalid_{timestamp}.json"
        with open(quarantine_file, 'w', encoding='utf-8') as f:
            json.dump(invalid_entries, f, ensure_ascii=False, indent=2)
        print(f"Обнаружено {len(invalid_entries)} невалидных записей в {quarantine_file}")
    
    return {
        "valid": len(valid_entries),
        "invalid": len(invalid_entries),
        "duplicates": len(data) - len(valid_entries) - len(invalid_entries)
    }

if __name__ == "__main__":
    stats = process_raw_data()
    print(f"\nИтоговая статистика:")
    print(f"- Уникальных валидных записей: {stats['valid']}")
    print(f"- Невалидных записей: {stats['invalid']}")
    print(f"- Дубликатов: {stats['duplicates']}")