from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


class ErrorLog(models.Model):
    """
        Model for storing error logs in db
        Fields:
            *date: date on which the error was captured.
            *message: string message that was logged.
    """
    date = models.DateField(auto_now=True)
    message = models.TextField()

    def __str__(self):
        return str(self.date)


class AccessLog(models.Model):
    """
        Model to store any action made by a user in the system.
        Fields:
            *date: date of access
            *user_id: id of user
            *content_type, object_id, and content_object is used for dynamic foreign key relation
            *event: name of event
            *extra_event: store any event not mentioned in choices
        
        Dynamic foreign key relation:
            If we have to keep logs of user creating an object in a model, 
            we need to get the following details of that created object:
                content_type of model - this can be fetched using:
                    ```
                        from django.contrib.contenttypes.models import ContentType
                        ctype = ContentType.objects.get(model="model_name")
                        # ctype will give the content_type for the model
                    ```
                object_id - this is the id of the object that we want to relate to
    """
    EVENT_CHOICES = [
        ("add", "add"),
        ("retrieve", "retrieve"),
        ("update", "update"),
        ("delete", "delete"),
        ("login", "login"),
        ("logout", "logout"),
        ("password_change", "password_change"),
        ("password_reset", "password_reset"),
        ("profile_change", "profile_change")
    ]
    date = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField(null=True, blank=True)

    # for dynamic foreign keys
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey("content_type", "object_id")

    event = models.CharField(choices=EVENT_CHOICES, max_length=20, null=True, blank=True)
    extra_event = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.date) + "- userid: " + str(self.user_id) + " " + str(self.event)


class ExceptionLog(models.Model):
    """
        Stores exception messages for a date.
    """
    date = models.DateTimeField(auto_now=True)
    message = models.TextField()

    def __str__(self):
        return str(self.date)


class EmailRecipients(models.Model):
    """
        Store list of recipients for emails
    """
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.email
