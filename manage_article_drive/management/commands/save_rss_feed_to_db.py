import json
import urllib

from django.core.management.base import BaseCommand, CommandError
import re
from django.utils import timezone
from webpreview import web_preview

from manage_article_drive.management.read_rss import reader
from manage_article_drive.models import Article, Tag


class Command(BaseCommand):
    help = 'Save tmp saved_articles from list of rss feed'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        #TODO: read file path propperly
        with open("/Users/yaelgree/article_drive/manage_article_drive"
                  "/management/commands/rss_url_list.txt", 'r') as r_f:
            for url_data in r_f:
                url_data = re.split(r'\t+', url_data.rstrip())
                raw_data = reader.read(url_data[1])
                for line in raw_data:
                    link = line[2]
                    m = re.search('https://www.google.com/url?.*url=('
                                  'https://.*)&ct=ga&cd=.*',
                                  line[2])
                    if m:
                        link = m.group(1)
                    title, description, image = web_preview(link)
                    if image is None:
                        image = "https://www.freeiconspng.com/uploads/no-image-icon-6.png"
                    try:
                        tag = Tag.objects.get(tag_text=url_data[0])
                    except Tag.DoesNotExist:
                        tag = Tag(tag_text=url_data[0])
                        tag.save()
                    article = Article(pub_date=timezone.now(),
                                            title_text=line[0],
                                            summary_text=line[1],
                                            link_text=link,
                                            image_url = image,
                                            state=0)
                    article.save()
                    article.tags.add(tag)
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully saved article. title: "%s"'%
                        article.title_text))