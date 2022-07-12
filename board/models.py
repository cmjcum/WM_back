from django.db import models


class Article(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    planet = models.ForeignKey('user.Planet', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)
    content = models.TextField()
    picture_url = models.URLField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.planet.name} | {self.author.nickname}]  {self.title}'


class Comment(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.parent == None:
            return f'[{self.article.title}]  {self.content}'

        return f'[{self.article.title}]  {self.content} ({self.parent.id}의 대댓글)'