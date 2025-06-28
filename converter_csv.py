import json
import csv
from pathlib import Path
from datetime import datetime

def convert_json_to_csv(json_file: Path, output_dir: Path = Path("output/csv")):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        print(f"Файл {json_file} не содержит данных для конвертации")
        return
    
    all_fields = set()
    for item in data:
        all_fields.update(item.keys())
    
    csv_fields = [field for field in sorted(all_fields) if not field.startswith('_')]
    
    meta_fields = [field for field in sorted(all_fields) if field.startswith('_')]
    fieldnames = csv_fields + meta_fields
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = output_dir / f"{json_file.stem}_{timestamp}.csv"
    
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in data:
            cleaned_row = {k: v for k, v in row.items() if v is not None}
            writer.writerow(cleaned_row)
    
    print(f"Успешно конвертировано в {csv_file}")
    return csv_file

def process_all_validated_files(json_dir: Path = Path("output/validated")):
    if not json_dir.exists():
        print(f"Директория {json_dir} не существует")
        return []
    
    converted_files = []
    for json_file in json_dir.glob('*.json'):
        try:
            csv_file = convert_json_to_csv(json_file)
            if csv_file:
                converted_files.append(csv_file)
        except Exception as e:
            print(f"Ошибка при обработке {json_file}: {str(e)}")
    
    return converted_files

if __name__ == "__main__":
    print("Начало конвертации JSON в CSV...")
    processed_files = process_all_validated_files()
    
    if not processed_files:
        print("Не найдено JSON файлов для конвертации")
    else:
        print(f"\nУспешно конвертировано {len(processed_files)} файлов:")
        for file in processed_files:
            print(f"- {file}")