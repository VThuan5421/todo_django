from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length = 200)
    #completed = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.title) > 100:
            return self.title[:100] + "..."
        else:
            return self.title

class Human(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job = models.CharField(max_length = 100, null = True, blank = True)

    def __str__(self):
        return str(self.user) + " - " + str(self.user.first_name) + " " + str(self.user.last_name)

class Creator(models.Model):
    human = models.ForeignKey(Human, on_delete = models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        etc = ""
        if len(self.task.title) > 80:
            etc = "..."
        return str(self.human.user.first_name) + " " + str(self.human.user.last_name)+ ' created "' + str(self.task.title[:80]) + etc + '"'