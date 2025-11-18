from os import name
from sys import modules
from django.db import models
from django.db.models.fields import related
from django.db.models.functions import Mod
from contracts.models import Contracts
from django.contrib.auth.models import User

from tasksboard.views import board
import cups
# Create your models here.

class Default(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Board(Default):
    name = models.CharField(max_length=50)
    description = models.TextField()
    contract = models.OneToOneField(Contracts, on_delete=models.CASCADE, related_name='contract_board', blank=True, null=True)


    def __str__(self):
        return self.name

class List(Default):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name


class Card(Default):
    list= models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    position = models.PositiveIntegerField(default=0)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_cards')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

class Comment(Default):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card')
    content = models.TextField()
    extra = models.JSONField()

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.card.title}"
