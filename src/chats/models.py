from django.db import models
from service.models import (
    UUIDModel,
    TimeCreateModel,
    TimeCreateUpdateModel,
    AccountForeignModel,
)
from django.contrib.contenttypes.fields import GenericRelation

# TODO: change folder path


def get_group_preview_file_path(instance, *_, **__) -> str:
    return instance.created.strftime("uploads/chat_previews/%Y/%m/%d/") + str(instance.id)  # type: ignore


# TODO: change folder path
def get_message_img_file_path(instance, *_, **__) -> str:
    return instance.created.strftime("uploads/message_img/%Y/%m/%d/") + str(instance.id)    # type: ignore


class ChatType(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название чата")

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип чата"
        verbose_name_plural = "Тип чата"


class ChatManager(models.Manager):
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("owner", "owner__user", "location_coordinate", "type")
            .prefetch_related("messages")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .select_related("owner", "owner__user", "location_coordinate", "type")
            .prefetch_related("messages")
            .all()
        )


class Chat(TimeCreateUpdateModel, UUIDModel):
    """
    Chat model.
    """
    type = models.ForeignKey(
        ChatType,
        related_name="chats",
        on_delete=models.PROTECT,
        verbose_name="Тип чата",
    )
    owner = models.ForeignKey(
        "users.Account",
        on_delete=models.SET_NULL,
        verbose_name="Создатель группы",
        related_name="owner_chat",
        null=True,
        blank=True,
    )
    members = models.ManyToManyField("users.Account", blank=True)
    meeting_time = models.DateTimeField(
        verbose_name="Время встречи", blank=True, null=True
    )
    location_coordinate = models.ForeignKey(
        "coordinates.Coordinate",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Координаты",
    )
    img_preview = models.ImageField(upload_to=get_group_preview_file_path, null=True, blank=True)

    objects = models.Manager()
    chat_manager = ChatManager()

    def __str__(self):
        return f"{self.type.title}:{self.id}"

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class MessageManager(models.Manager):
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("chat", "account")
            .prefetch_related("reactions")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .select_related("chat", "account")
            .prefetch_related("reactions")
            .all()
        )


class Message(UUIDModel, TimeCreateModel, AccountForeignModel):
    """
    Message model. Fields: id, time_created,
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    account = models.ForeignKey(
        "users.Account",
        on_delete=models.CASCADE,
        verbose_name="Автор сообщения",
        related_name="messages",
    )
    text = models.TextField(max_length=500, verbose_name="Текст сообщения")
    img = models.ImageField(
        upload_to=get_message_img_file_path, null=True
    )  # TODO: added extra models FK
    viewed = models.BooleanField(default=False)
    reactions = GenericRelation("reactions.ReactionLike")
    objects = models.Manager()
    message_manager = MessageManager()

    def __str__(self):
        return f"Account: {self.account.id}, viewed: {self.viewed}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
