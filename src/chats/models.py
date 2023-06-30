from django.db import models
from service.models import (
    UUIDModel,
    TimeCreateModel,
    TimeCreateUpdateModel,
)
from users.models import Account


# TODO: change folder path
def get_group_preview_file_path(instance, *_, **__) -> str:
    return instance.time_created.strftime("uploads/group_previews/%Y/%m/%d/") + str(instance.id)  # type: ignore


# TODO: change folder path
def get_message_img_file_path(instance, *_, **__) -> str:
    return instance.time_created.strftime("uploads/message_img/%Y/%m/%d/") + str(instance.id)  # type: ignore


class Group(TimeCreateUpdateModel, UUIDModel):
    title = models.CharField(max_length=100, verbose_name="Название Группы")
    owner = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        verbose_name="Создатель группы",
        related_name="groups_owner",
        null=True,
        blank=True,
    )
    members = models.ManyToManyField(Account, blank=True, related_name="groups")

    meeting_time = models.DateTimeField(verbose_name="Время встречи", blank=True, null=True)
    location_coordinate = models.ForeignKey(
        "coordinates.Coordinate",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Координаты",
    )
    img_preview = models.ImageField(upload_to=get_group_preview_file_path, null=True, blank=True)

    def __str__(self):
        return f"{self.title}:{self.id}"

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Chat(TimeCreateUpdateModel, UUIDModel):
    members = models.ManyToManyField("users.Account", blank=True, related_name="chats")

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name="Сообщение из чата", related_name="messages")
    message = models.ForeignKey(
        "Message",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"Сообщение из чата, автор:{self.message.account.id}"

    class Meta:
        index_together = [
            ["chat", "message"],
        ]


class GroupMessage(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, verbose_name="Сообщение из группы", related_name="messages"
    )
    message = models.OneToOneField(
        "Message",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"Сообщение из чата, автор:{self.message.account.id}"

    class Meta:
        index_together = [
            ["group", "message"],
        ]


class Message(UUIDModel, TimeCreateModel):
    account: Account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name="Автор сообщения",
        related_name="messages",
    )
    text = models.TextField(max_length=500, verbose_name="Текст сообщения")
    imgages = models.ManyToManyField("MessageImages", blank=True, related_name="message")
    viewed = models.BooleanField(default=False, verbose_name="Просмотрено?")
    reactions = models.ManyToManyField("reactions.Reaction", blank=True, related_name="messages")
    available = models.BooleanField(default=True, verbose_name="Доступно к прочтению")

    def __str__(self):
        return f"Автор: {self.account.user.username}, текст :{self.text}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def hide_message(self):
        self.available = False
        self.viewed = True
        self.save()


class MessageImages(UUIDModel, TimeCreateModel):
    img = models.ImageField(upload_to=get_message_img_file_path, null=True)

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Фотография из сообщения"
        verbose_name_plural = "Фотографии из сообщений"
