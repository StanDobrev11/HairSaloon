from django.contrib.auth import get_user_model
from django.db import models

from HairSaloon.common.validators import MinLengthValidator

UserModel = get_user_model()


class Comment(models.Model):
    TITLE_MAX_LENGTH = 100
    TITLE_MIN_LENGTH = 10
    TEXT_MAX_LENGTH = 500
    TEXT_MIN_LENGTH = 25

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        validators=[
            MinLengthValidator(TITLE_MIN_LENGTH),
        ]
    )

    text = models.TextField(
        max_length=TEXT_MAX_LENGTH,
        validators=[MinLengthValidator(TEXT_MIN_LENGTH)]
    )

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return f"{self.title} by {self.user}"
