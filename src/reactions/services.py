from django.contrib.contenttypes.models import ContentType
from reactions.models import ReactionLike


def add_like(obj, user, reaction_id=None):
    obj_type = ContentType.objects.get_for_model(obj)
    like = ReactionLike.objects.get_or_create(content_type=obj_type,
                                              object_id=obj.id, user=user, reaction=reaction_id)

    return like


def remove_like(obj, user, reaction_id=None):
    obj_type = ContentType.objects.get_for_model(obj)
    ReactionLike.objects.filter(content_type=obj_type, object_id=obj.id,
                                user=user, reaction=reaction_id).delete()


def is_fan(obj, user) -> bool:
    obj_type = ContentType.objects.get_for_model(obj)
    likes = ReactionLike.objects.filter(content_type=obj_type,
                                        object_id=obj.id, user=user)

    return likes.exists()


def get_fans(obj, user):
    return ReactionLike.objects.filter(object_id=obj.id, user=user)
