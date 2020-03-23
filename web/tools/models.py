from django.db import models, connection

#Create your models here.
# class ImageDetail(models.Model):
#     img_url = models.TextField(default='')
#     #tag_name = models.TextField()
#     file_path = models.TextField()
#     top1 = models.TextField()
#     top2 = models.TextField()
#     top3 = models.TextField()
#     visited = models.BooleanField(default=False)
def ImageDetail():
    with connection.cursor() as cursor:
        file_path = cursor.execute("SELECT file_path FROM ImageDetail")
        f = file_path.fetchall()
        top1 = cursor.execute("SELECT top1 FROM ImageDetail")
        t1 = top1.fetchall()
        top2 = cursor.execute("SELECT top2 FROM ImageDetail")
        t2 = top2.fetchall()
        top3 = cursor.execute("SELECT top3 FROM ImageDetail")
        t3 = top3.fetchall()
        prob1 = cursor.execute("SELECT prob1 FROM ImageDetail")
        p1 = prob1.fetchall()
        prob2 = cursor.execute("SELECT prob2 FROM ImageDetail")
        p2 = prob2.fetchall()
        prob3 = cursor.execute("SELECT prob3 FROM ImageDetail")
        p3 = prob3.fetchall()
    return f, t1, t2, t3, p1, p2, p3