from typing import Union

from django.db import models
from service.models import (
    UUIDModel,
    TimeCreateModel,
    TimeCreateUpdateModel,
    AccountForeignModel,
)
from users.models import Account


# TODO: change folder path
def get_group_preview_file_path(instance, *_, **__) -> str:
    return instance.time_created.strftime("uploads/chat_previews/%Y/%m/%d/") + str(instance.id)  # type: ignore


# TODO: change folder path
def get_message_img_file_path(instance, *_, **__) -> str:
    return instance.time_created.strftime("uploads/message_img/%Y/%m/%d/") + str(instance.id)    # type: ignore


class GroupManager(models.Manager):
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("owner", "owner__user", "coordinate")
            .prefetch_related("messages", "members")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .select_related("owner", "owner__user", "coordinate")
            .prefetch_related("messages", "members")
            .all()
        )

    def create_group(self, title, account):
        new_group = self.model(title=title)
        new_group.save(using=self._db)

        if account:
            new_group.owner = account
            new_group.members.add(account)
            if account.coordinate:
                new_group.coordinate = account.coordinate
            new_group.save()
        return new_group


class Group(TimeCreateUpdateModel, UUIDModel):
    """
    Group model.
    """
    title = models.CharField(max_length=100, verbose_name="Название Группы")
    owner = models.ForeignKey(
        to=Account,
        on_delete=models.SET_NULL,
        verbose_name="Создатель группы",
        related_name="groups_owner",
        null=True,
        blank=True,
    )
    members = models.ManyToManyField(
        to=Account,
        blank=True,
        related_name="groups",
        verbose_name="Участники группы"
    )
    meeting_time = models.DateTimeField(verbose_name="Время встречи", blank=True, null=True)
    coordinate = models.ForeignKey(
        "coordinates.Coordinate",
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Координаты",
    )
    img_preview = models.ImageField(
        verbose_name="Аватар группы",
        upload_to=get_group_preview_file_path,
        null=True,
        blank=True
    )

    objects = models.Manager()
    group_manager = GroupManager()

    def get_image_preview_url(self) -> str:
        if not self.img_preview:
            return "..."  # default image url
        return self.img_preview.url

    def get_members_count(self) -> int:
        return self.members.count()

    def __str__(self):
        return f"{self.title}:{self.id}"

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class ChatManager(models.Manager):
    def get(self, *args, **kwargs):
        return (
            super()
            .prefetch_related("messages", "members")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .prefetch_related("messages", "members")
            .all()
        )


CHAT_TYPE = (
    ("STND", "Стандартный чат 1-1"),
    ("CSTM", "Кастомный чат любое кол-во людей"),
)


class Chat(TimeCreateUpdateModel, UUIDModel):
    """
    Chat model.
    """
    type = models.CharField(
        verbose_name="Тип чата",
        max_length=4,
        choices=CHAT_TYPE,
        default="STND"
    )

    members = models.ManyToManyField(
        verbose_name='Участники чата',
        to="users.Account",
        blank=True,
        related_name='chats'
    )

    objects = models.Manager()
    chat_manager = ChatManager()

    def __str__(self):
        return f"{self.type.title}:{self.id}"

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class ChatMessage(models.Model):
    """
    Model for chat and message relation.
    """
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, verbose_name="Чат", related_name="messages")
    message = models.ForeignKey(
        to="Message",
        on_delete=models.CASCADE,
        verbose_name="Содержание сообщения",
        related_name='chats'
    )

    def __str__(self) -> str:
        return f"Сообщение из чата, автор:{self.message.account.id}"

    class Meta:
        index_together = [
            ["chat", "message"],
        ]


class GroupMessageManager(models.Manager):
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("group", "message", "message__account", "message__account__user", "message__reactions")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .select_related("group", "message", "message__account", "message__account__user", "message__reactions")
            .all()
        )

    def create(self, account, text, group, available: bool = True):
        group_message = super().create(
            group=group,
            message=Message.message_manager.create(
                account=account,
                text=text,
                available=available
            )
        )
        return group_message


class GroupMessage(models.Model):
    """
    Model for group and message relation.
    """
    group = models.ForeignKey(
        to=Group, on_delete=models.CASCADE, verbose_name="Группа", related_name="messages"
    )
    message = models.OneToOneField(
        "Message",
        on_delete=models.CASCADE,
        verbose_name="Содержание сообщения"
    )

    objects = models.Manager()
    group_message_manager = GroupMessageManager()

    def __str__(self) -> str:
        return f"Сообщение из чата, автор:{self.message.account.id}"

    class Meta:
        index_together = [
            ["group", "message"],
        ]


class MessageManager(models.Manager):
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("account")
            .prefetch_related("reactions", "media_files")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .select_related("account")
            .prefetch_related("reactions", "media_files")
            .all()
        )

    def create(self, account, text, available: bool = True):
        message = super().create(
            account=account,
            text=text,
            available=available
        )
        return message


class Message(UUIDModel, TimeCreateModel, AccountForeignModel):
    """
    Message model. Fields: id, time_created,
    """
    account = models.ForeignKey(
        to="users.Account",
        on_delete=models.CASCADE,
        verbose_name="Автор сообщения",
        related_name="messages",
    )
    text = models.TextField(max_length=500, verbose_name="Текст сообщения")
    media_files = models.ManyToManyField(
        to="MessageMediaFile", blank=True, related_name="message", verbose_name="Приложения к сообщению")
    viewed = models.BooleanField(default=False, verbose_name="Просмотрено?")
    reactions = models.ManyToManyField(
        to="reactions.Reaction", related_name="messages", verbose_name="Реакция на сообщение"
    )
    available = models.BooleanField(default=True, verbose_name="Доступно к прочтению")

    objects = models.Manager()
    message_manager = MessageManager()

    def __str__(self):
        return f"Account: {self.account.id}, viewed: {self.viewed}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class MessageMediaFile(UUIDModel, TimeCreateModel):
    """
    Model for media files of messages.
    #TODO Добавим изначально только фотографии, после - можно добавить аудио/видео/доки
    """

    img = models.ImageField(upload_to=get_message_img_file_path, null=True)

    def __str__(self):
        return f"Медиафайл к сообщению {self.message.id}"

    class Meta:
        ordering = ["-time_created"]
        verbose_name = "Приложение к сообщению"
        verbose_name_plural = "Приложения к сообщениям"
