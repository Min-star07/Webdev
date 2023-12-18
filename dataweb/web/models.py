from django.db import models
from datetime import datetime
#python manage.py makemigrations
#python manage.py migrate
#增：models.User.create()
#查：models.User.objects.filter()
#.first()取第一条数据
# .all()
#删除models.User.objects.all().delete()
#改：models.User.objects.filter().update()
class User(models.Model):
    # ID = models.IntegerField(max_length=50) #密码
    username = models.CharField(max_length=50)  # 用户账号
    emailname = models.CharField(max_length=50)  # 用户邮箱
    password = models.CharField(max_length=255) #密码
    # password_hash = models.CharField(max_length=100)  # 密码
    # password_salt = models.CharField(max_length=50)  # 密码干扰值
    # status = models.IntegerField(default=1)  # 状态:1正常/2禁用/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间
    #
    # def toDict(self):
    #     return {'id': self.id, 'username': self.username, 'nickname': self.nickname,
    #             'password_hash': self.password_hash, 'password_salt': self.password_salt, 'status': self.status,
    #             'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
    #             'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    #
    # class Meta:
    #     db_table = "user"  # 更改表名
