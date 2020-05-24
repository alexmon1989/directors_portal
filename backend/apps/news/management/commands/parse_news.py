from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pytils.translit import slugify
from apps.news.models import News
import requests
from xml.dom.minidom import parse, parseString
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
import os
import datetime
import pathlib


class Command(BaseCommand):
    help = 'Gets news from monm.rk.gov.ru'

    def handle(self, *args, **options):
        r = requests.get("http://monm.rk.gov.ru/rss")
        dom = parseString(r.content)
        items = dom.getElementsByTagName('item')
        for item in items:
            title = item.getElementsByTagName('title')[0].firstChild.data
            slug = slugify(title)
            description = item.getElementsByTagName('description')[0].firstChild.data
            pub_date = parsedate_to_datetime(item.getElementsByTagName('pubDate')[0].firstChild.data)
            link = item.getElementsByTagName('link')[0].firstChild.data
            
            if News.objects.filter(title=title).count() == 0:
                r = requests.get(link)
                soup = BeautifulSoup(r.content, 'lxml')
                
                text_div = soup.find('div', class_='info')
                text_inner_html = "".join([str(x) for x in text_div.contents]) 
                
                image_div = soup.find('div', class_='slider-photo _nowid')
                image_el = image_div.find('img')
                
                response = requests.get(image_el.attrs['src'])
                
                now = datetime.datetime.now()
                img_path = os.path.join(
                    settings.MEDIA_ROOT, 
                    "news", 
                    str(now.year), 
                    str(now.month), 
                    str(now.day)
                )
                pathlib.Path(img_path).mkdir(parents=True, exist_ok=True)
                img_path = os.path.join(img_path, f"{slug}.jpg")
                
                file = open(img_path, "wb")
                file.write(response.content)
                file.close()
                
                News.objects.create(
                    title=title, 
                    slug=slugify(title), 
                    short_text=description, 
                    full_text=text_inner_html, 
                    published_at=pub_date,
                    image=os.path.join("news", str(now.year), str(now.month), str(now.day), f"{slug}.jpg")
                )
            
        self.stdout.write(self.style.SUCCESS('Success'))
