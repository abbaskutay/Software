from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import misaka


from groups.models import Group


from django.contrib.auth import get_user_model
User = get_user_model()


class Expense(models.Model):
    user = models.ForeignKey(User, related_name="expenses")
    created_at = models.DateTimeField(auto_now=True)
    title = models.TextField()
    title_html = models.TextField(editable=False)
    cost = models.TextField()
    cost_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="expenses",null=
                              True,blank=True)

    def __str__(self,*args, **kwargs):
        return self.title


    def save(self, *args, **kwargs):
        self.title_html = misaka.html(self.title)
        self.cost_html = misaka.html(self.cost)

        super(Expense, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "expenses:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        # unique_together = ["user", "title"]
