from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class TagManager(models.Manager):
    pass


class AnswerManager(models.Manager):
    def sorted_by_created_at(self):
        return self.order_by('-created_at')

    def get_answers_for_question(self, question_id):
        return self.filter(question_id=question_id)


class QuestionManager(models.Manager):
    def sorted_by_created_at(self):
        return self.order_by('-created_at')

    def get_hot_questions(self):
        return self.annotate(l_count=Count('likes')).order_by('-l_count')

    def filter_by_tag(self, slug):
        return self.filter(tags__name=slug).order_by('-created_at')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/', null=False, blank=False, default='no-profile-picture-icon.jpg')
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(User, related_name='liked_questions')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_answers_count(self):
        return Answer.objects.filter(question_id=self.id).count()

    def get_likes_count(self):
        return self.likes.count()


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_answers')
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer to '{self.question}'"

    def get_likes_count(self):
        return self.likes.count()