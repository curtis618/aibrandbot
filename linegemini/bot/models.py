from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=100, verbose_name="活動名稱")
    end_date = models.DateField(verbose_name="活動結束日期")
    location = models.CharField(max_length=100, verbose_name="地點")
    description = models.TextField(verbose_name="描述")
    image_url = models.URLField(verbose_name="圖片網址", blank=True, null=True)
    activity_link = models.TextField(verbose_name="活動連結", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "活動"
        verbose_name_plural = "活動列表"
