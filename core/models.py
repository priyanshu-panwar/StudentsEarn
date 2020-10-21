from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail 
from django.conf import settings

class Category(models.Model):
	Title = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.Title


class EmailID(models.Model):
	Email = models.EmailField()
	Password = models.CharField(max_length=100)
	Subject = models.ForeignKey(Category, on_delete=models.CASCADE)
	is_alloted = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.Email}'

"""
class User(AbstractUser):
	id_alloted = models.ForeignKey(EmailID, on_delete=models.CASCADE, null=True, blank=True)
	subject = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	is_active = models.BooleanField(default=False)
	mobile_number = models.CharField(max_length=13, null=True, blank=True)
	rank = models.CharField(max_length=5, null=True, blank=True)
	Files = models.FileField(upload_to='files/', null=True, blank=True)
"""

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	upi = models.CharField(max_length=100, default='...@upi')
	balance = models.IntegerField(default=0)
	questions_this_month = models.IntegerField(default=0)
	id_alloted = models.ForeignKey(EmailID, on_delete=models.CASCADE, null=True, blank=True)
	subject = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	is_active = models.BooleanField(default=False)
	mobile_number = models.CharField(max_length=13, null=True, blank=True)
	rank = models.CharField(max_length=5, null=True, blank=True)
	Files = models.FileField(upload_to='files/', null=True, blank=True)

	class Meta:
		verbose_name_plural = "Profiles"
		ordering = ['-questions_this_month',]

	def __str__(self):
		return self.upi


class Transaction(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	credit = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user}'

	def save(self, *args, **kwargs):
		self.user.balance += self.credit
		self.user.save()
		if (self.credit != 0):
			print("mailing now...")
			subject = 'Hard Work Pays - StudentsEarn'
			message = f'Hi {self.user.user.username}, We have credited Rs.{self.credit} to your account.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [self.user.user.email, ]
			print(email_from)
			print(recipient_list)
			send_mail( subject, message, email_from, recipient_list )
		super(Transaction, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()