from django.db import models
from jsonfield import JSONField
from uuidfield import UUIDField


class Order(models.Model):
    STATUS_CREATED = 'created'
    STATUS_COMPILING = 'compiling'
    STATUS_COMPILED = 'compiled'
    STATUS_UPLOADED = 'uploaded'
    STATUS_NOTIFIED = 'notified'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_CREATED, 'The order has been created.'),
        (STATUS_COMPILING, 'The order is being compiled.'),
        (STATUS_COMPILED, 'The order has been compiled.'),
        (STATUS_UPLOADED, 'The order has been uploaded to Shapeways.'),
        (STATUS_NOTIFIED, 'The customer has been notified by e-mail.'),
        (STATUS_FAILED, 'Something went wrong.'),
    ]

    uuid = UUIDField(auto=True)
    params = JSONField()
    digits = models.CharField(max_length=5)
    material = models.PositiveIntegerField()
    email = models.EmailField()
    shapeways_url = models.URLField(blank=True)
    compile_job_id = models.CharField(max_length=36, blank=True)
    upload_job_id = models.CharField(max_length=36, blank=True)
    email_job_id = models.CharField(max_length=36, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CREATED)

    def __repr__(self):
        return "<Order '{0}'>".format(self.uuid)

