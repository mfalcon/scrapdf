# scrapdf
Proyecto para extraer de una página el texto de archivos del tipo pdf. Se usa Python con la librería Scrapy. Usa [tesseract](https://github.com/tesseract-ocr/tesseract)
como librería de OCR, por lo que tiene que estar previamente instalada.

Para correrlo van a necesitar alguna distribución de Python con pip para instalar las dependencias. Podés hacerlo con el siguiente comando:

```bash
pip install -r requirements.txt
```
Para correr el crawler:

```bash
scrapy crawl scrapdf
```
Para correr el crawler y guardar los resultados en un archivo json:

```bash
scrapy crawl scrapdf -o example.json
```
