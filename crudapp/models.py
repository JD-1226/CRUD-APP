from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
class Record(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    Class = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=Record)
def save_to_mongo(sender, instance, **kwargs):
    record_dict = {
        "id": instance.id,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "Class": instance.Class,
        "phone_number": instance.phone_number,
        "address": instance.address,
        "state": instance.state,
        "city": instance.city,
        "created_at": instance.created_at.isoformat() if instance.created_at else None,
    }
    settings.MONGO_COLLECTION.update_one(
        {"id": instance.id}, {"$set": record_dict}, upsert=True
    )


@receiver(post_delete, sender=Record)
def delete_from_mongo(sender, instance, **kwargs):
    settings.MONGO_COLLECTION.delete_one({"id": instance.id})