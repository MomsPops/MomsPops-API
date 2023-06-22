from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

from .city import City


# class AccountManager(models.Manager):
#     def create_account(
#         self,
#         city_name: str,
#         country_name: str,
#         user: dict[str, str]
#     ):
#         city = City.objects.get(
#             name=city_name, country__name=country_name
#         )  # TODO: need unique fields
#         new_user = User.objects.create_user(**user)
#         new_account = self.model(user=new_user, city=city)
#         new_account.save(using=self._db)
#         return new_account


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)

    bio = models.TextField(blank=True, null=True, verbose_name="Биография")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="День рождения")
    photo = models.ImageField(
        upload_to="uploads/account_img/", verbose_name="Фото", blank=True, null=True
    )
    status = models.CharField(max_length=100, verbose_name="Статус", blank=True)

    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Город")
    black_list = models.ManyToManyField("self", blank=True, verbose_name="Игнор лист")
    # objects = AccountManager()

    def __str__(self):
        return self.user.username
