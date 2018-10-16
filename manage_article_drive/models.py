from django.db import models

class Tag(models.Model):
    tag_text = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_text

class Article(models.Model):
    pub_date = models.DateTimeField('date published')
    title_text = models.CharField(max_length=200)
    summary_text = models.CharField(max_length=1000)
    link_text = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    state = models.IntegerField(default=0)
    #0 - no choice has been made, 1 - Save it, 2 discard it

    def __str__(self):
        return "Title:"+self.title_text

event_date = models.DateField(blank=False,)
