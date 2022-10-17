from django.db import models
from taggit.managers import TaggableManager

class Post(models.Model):
    writer = models.ForeignKey('users.User', verbose_name='작성자', on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=50)
    content = models.TextField('내용', max_length=400)
    tags = TaggableManager(verbose_name='해쉬태그', blank=True) 
    views = models.PositiveIntegerField('조회수', default=0)
    created_date = models.DateTimeField('생성시간', auto_now_add=True)
    updated_date = models.DateTimeField('수정시간', auto_now=True)
    is_active = models.BooleanField('활성화', default=True)

    def __str__(self):
        return f'{self.writer} 님의 글 : {self.title}'
    
    @property
    def update_views(self):
        self.views = self.views + 1
        self.save()
        
class Like(models.Model):
    user = models.ForeignKey('users.User', verbose_name='사용자', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='게시글', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} ❤️ {self.post}'