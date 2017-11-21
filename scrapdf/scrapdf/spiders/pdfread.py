import datetime
import io
import json

import pyocr
import pytesseract
import requests
import scrapy
from PIL import Image
from wand.image import Image as Img

from scrapdf.items import PdfItem


def parse_pdf(pdf_name, pdf_content):
    fname = pdf_name + '.pdf'
    with open(fname, 'wb') as f:
        f.write(pdf_content)
    
    #antes de hacer ocr, hay que convertir el pdf a imagen, una por pagina
    image_pdf = Img(filename=fname, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')
    
    req_image = []
    #extraer la data de las imagenes de cada pagina una por una
    for img in image_jpeg.sequence:
        img_page = Img(image=img)
        req_image.append(img_page.make_blob('jpeg'))
    
    final_text = []
    #procesar las imagenes y extraer texto con tesseract
    for img in req_image:
        text = pytesseract.image_to_string(Image.open(io.BytesIO(img)))
        final_text.append(text)
    
    return final_text


class PdfSpider(scrapy.Spider):
    name = "scrapdf"

    def start_requests(self):
        
        urls = [
            'http://chequeado.com/justiciapedia/profiles/adriana-palliotti/#',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)

    def parse_seccion(self, response):
        #obtener todos los links que tengan .pdf en su url
        pdf_links = response.xpath('//a[contains(@href, ".pdf")]/@href').extract()
        absolute_pdf_links = [response.urljoin(pdf_link) for pdf_link in pdf_links]
        for pdf_link in absolute_pdf_links:
            res = requests.get(pdf_link)
            pdf_name = pdf_link.split('/')[-1].replace('.pdf','').replace('%20','')
            parsed_text = parse_pdf(pdf_name, res.content)
            
            item = PdfItem()
            item['pdf_link'] = pdf_link
            item['full_text'] = ' ***next page*** '.join([e for e in parsed_text]) 
            yield item
        
    
