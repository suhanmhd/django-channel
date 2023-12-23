from django.db import models
from djongo import models as djongo_models
from dbuserapp.models import User

class Documents(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_str = str(self.user.username) if self.user else "No User"
        return f"{user_str}-{self.title}"
    
    def to_json(self):
        return {
            '_id': str(self._id),
            'user': self.user.username if self.user else None,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
