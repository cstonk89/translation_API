# Overview

This repo is for a translation API built in Python serving a main endpoint called "translate" via FastAPI. The endpoint takes in a request consistent of a
string (text to be translated) and a target language. The translation model used is Facebook's m2m100_418M, this model is loaded upon startup of the endpoint and is a many-to-many translation model supporting languages such as:

| Code | Language        |
| ---- | --------------- |
| af   | Afrikaans       |
| am   | Amharic         |
| ar   | Arabic          |
| ast  | Asturian        |
| az   | Azerbaijani     |
| ba   | Bashkir         |
| be   | Belarusian      |
| bg   | Bulgarian       |
| bn   | Bengali         |
| br   | Breton          |
| bs   | Bosnian         |
| ca   | Catalan         |
| ceb  | Cebuano         |
| cs   | Czech           |
| cy   | Welsh           |
| da   | Danish          |
| de   | German          |
| el   | Greek           |
| en   | English         |
| es   | Spanish         |
| et   | Estonian        |
| fa   | Persian         |
| ff   | Fulah           |
| fi   | Finnish         |
| fr   | French          |
| fy   | Western Frisian |
| ga   | Irish           |
| gd   | Scottish Gaelic |
| gl   | Galician        |
| gu   | Gujarati        |
| ha   | Hausa           |
| he   | Hebrew          |
| hi   | Hindi           |
| hr   | Croatian        |
| ht   | Haitian Creole  |
| hu   | Hungarian       |
| hy   | Armenian        |
| id   | Indonesian      |
| ig   | Igbo            |
| ilo  | Iloko           |
| is   | Icelandic       |
| it   | Italian         |
| ja   | Japanese        |
| jv   | Javanese        |
| ka   | Georgian        |
| kk   | Kazakh          |
| km   | Khmer           |
| kn   | Kannada         |
| ko   | Korean          |
| lb   | Luxembourgish   |
| lg   | Ganda           |
| ln   | Lingala         |
| lo   | Lao             |
| lt   | Lithuanian      |
| lv   | Latvian         |
| mg   | Malagasy        |
| mk   | Macedonian      |
| ml   | Malayalam       |
| mn   | Mongolian       |
| mr   | Marathi         |
| ms   | Malay           |
| my   | Burmese         |
| ne   | Nepali          |
| nl   | Dutch           |
| no   | Norwegian       |
| ns   | Northern Sotho  |
| oc   | Occitan         |
| or   | Oriya           |
| pa   | Punjabi         |
| pl   | Polish          |
| ps   | Pashto          |
| pt   | Portuguese      |
| ro   | Romanian        |
| ru   | Russian         |
| sd   | Sindhi          |
| si   | Sinhala         |
| sk   | Slovak          |
| sl   | Slovenian       |
| so   | Somali          |
| sq   | Albanian        |
| sr   | Serbian         |
| ss   | Swati           |
| su   | Sundanese       |
| sv   | Swedish         |
| sw   | Swahili         |
| ta   | Tamil           |
| th   | Thai            |
| tl   | Tagalog         |
| tn   | Tswana          |
| tr   | Turkish         |
| uk   | Ukrainian       |
| ur   | Urdu            |
| uz   | Uzbek           |
| vi   | Vietnamese      |
| wo   | Wolof           |
| xh   | Xhosa           |
| yi   | Yiddish         |
| yo   | Yoruba          |
| zh   | Chinese         |
| zu   | Zulu            |

There is also a "supported_languages" endpoint to view which languages the API supports.

## Usage

The main endpoint in this app is the translation endpoint, this endpoint takes in source_text, source_language and target_language parameters, the source_text is checked
for profanity via a helper function and the source and target language parameters are checked against the model's supported languages to ensure they are supported. This project is managed by Poetry and runs on Python version 3.12.5, the project can be installed via running `poetry install` in the root directory. I would recommend using Pyenv to set a local Python version variable and running `poetry env use $(pyenv which python)` if you are having difficulty with forcing Poetry to use the correct Python version.

The app can be started via the command `poetry run uvicorn src.app:app --reload --host 127.0.0.1 --port 8000` if you don't want other machines to be able to send requests to your endpoint, alternatively running the server via `poetry run uvicorn src.app:app --reload --host 0.0.0.0 --port 8000` will allow others to send requests to your endpoint.

The endpoint accepts requests like so:

```curl -X POST http://127.0.0.1:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "source_text": "Hello, how are you?",
    "source_language": "en",
    "target_language": "fr"
  }'
```

and will return outputs in the following format:

`{"source_text":"Hello, how are you?","source_language":"en","target_language":"fr","translation":"Bonjour, comment vous êtes-vous ?"}`

### Further improvements

Tracing and observability: Attempted to integrate tracing/observability via Arize phoenix/Langfuse ran into large dependency issues with both, idea was to track key metrcis such as latency to provide a view of how this metric changes over time.

Vector databases: In the future would store embedded inputs and outputs to track statistical changes in input feature distribution for example by clustering inputs and mapping centroid coordinates and tracking how the coordinates change over time (7,14,28 day periods for example). Additionally, gives the opportunity to track precision, recall, F1 score and calibrate model via finetuning in the future.

Small UI/GUI: Mainly a UX feature, but would like to give users an opportunity to record their feelings via feedback prompts in the GUI/UI around things like accuracy, ease of use and latency. Using the same inference run ID for the user feedback, tracing/observability and vector embeddings, these seperate pieces of data could be
collected together in a relational database using the inference run ID as a primary key to view an high granularity look at the service from several perspectives.
