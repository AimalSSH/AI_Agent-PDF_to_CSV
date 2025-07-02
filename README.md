# AI Agent - PDF to CSV
AI Agent that extracts the necessary information from a PDF file for the user and converts it into CSV format

## How to launch
Go to two directories:
   1. AI_Agent-PDF_to_CSV/config/ai_config.yaml
   2. AI_Agent-PDF_to_CSV/core/config/ai_config.yaml

There are two configuration files here that we need to add to the graph `api_key: ""` You can get your own key on the website https://openrouter.ai/

You can choose a model ` model: "deepseek/deepseek-chat"`, The default value is `deepseek/deepseek-chat`

To download all the libraries, use `pip install -r requirements.txt`

Here, upload your PDF document with the name "example" `AI_Agent-PDF_to_CSV\data`

Next, you need to run the file `main.py`. 

# AI-агент - преобразование PDF в CSV
AI-агент, который извлекает необходимую информацию из PDF-файла для пользователя и преобразует ее в формат CSV

## Как запустить
Перейдите к двум каталогам:
 1. AI_Agent-PDF_to_CSV/config/ai_config.yaml
 2. AI_Agent-PDF_to_CSV/core/config/ai_config.yaml

Здесь есть два файла конфигурации, которые нам нужно добавить в графу `"api_key: ""` Вы можете получить свой собственный ключ на веб-сайте https://openrouter.ai/

Вы можете выбрать модель `model: "deepseek/deepseek-chat"` значение по умолчанию `deepseek/deepseek-chat`

Загрузить все библиотеки, использовать `pip install -r requirements.txt`

Здесь загрузите свой PDF-документ с именем "example" `AI_Agent-PDF_to_CSV\data`

Далее вам нужно запустить файл `main.py`.
