from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    followedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followedBy"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    def __str__(self):
        return f"{self.followedBy.id} follows {self.following.id}"
