from django.db import models

from auth.models import User


class File(models.Model):
    name = models.CharField(max_length=128)
    file_id = models.CharField(max_length=10)
    owner = models.ForeignKey(User,
                              models.CASCADE,
                              related_name='files',
                              db_column='owner_id')
    coowners = models.ManyToManyField(User,
                                      related_name='cofiles',
                                      through='FilePermission',
                                      through_fields=('file', 'user'))

    def check_permissions(self, user):
        return user == self.owner or user in self.coowners.all()

    class Meta:
        managed = False
        db_table = 'file'


class FilePermission(models.Model):
    file = models.ForeignKey(File,
                             on_delete=models.CASCADE,
                             related_name='file_permissions',
                             db_column='file_id')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='file_permissions',
                             db_column='user_id')

    class Meta:
        managed = False
        db_table = 'file_permission'
