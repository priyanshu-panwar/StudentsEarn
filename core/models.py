from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail 
from django.conf import settings
from PIL import Image
from django.template import loader

class SendMessage(models.Model):
	subject = models.CharField(max_length=200)
	message = models.TextField()
	assigned_users = models.BooleanField(default=False)
	non_assigned_users = models.BooleanField(default=False)
	all_active = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.subject

	class Meta:
		verbose_name = "Send Messages To Students"
		ordering = ['-date']

	def save(self, *args, **kwargs):
		if self.assigned_users:
			mailers = Profile.objects.filter(is_active=True)
			recipient_list = []
			for x in mailers:
				recipient_list.append(x.user.email)
			from_email = settings.EMAIL_HOST_USER
			send_mail(self.subject, self.message, from_email, recipient_list)
		if self.assigned_users:
			mailers = Profile.objects.filter(id_alloted__isnull=False)
			recipient_list = []
			for x in mailers:
				recipient_list.append(x.user.email)
			from_email = settings.EMAIL_HOST_USER
			send_mail(self.subject, self.message, from_email, recipient_list)
		if self.assigned_users:
			mailers = Profile.objects.filter(id_alloted__isnull=True)
			recipient_list = []
			for x in mailers:
				recipient_list.append(x.user.email)
			from_email = settings.EMAIL_HOST_USER
			send_mail(self.subject, self.message, from_email, recipient_list)
		super(SendMessage, self).save(*args, **kwargs)

class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField()
	reply = models.TextField(default='We will reply you soon.')
	date = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "MESSAGES"
		ordering = ['-date',]

	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		if self.reply != "We will reply you soon.":
			subject = "StudentsEarn - You have a message from Support."
			message = f"Hello {self.user.username}, \nPlease open your Profile. We have replied to your message - {self.message}.\n Our Support Said : {self.reply}."
			from_email = settings.EMAIL_HOST_USER
			recipient_list = [self.user.email, ]
			send_mail(subject, message, from_email, recipient_list)
		super(Message, self).save(*args, **kwargs)


class Category(models.Model):
	Title = models.CharField(max_length=100)
	price = models.IntegerField(default=30)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.Title


class EmailID(models.Model):
	Email = models.EmailField()
	Password = models.CharField(max_length=100)
	Subject = models.ForeignKey(Category, on_delete=models.CASCADE)
	is_alloted = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	release = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if self.release:
			pro = Profile.objects.filter(user=self.user)
			if (len(pro) > 0):
				pro = pro[0]
			pro.id_alloted = None
			pro.save()
			self.is_alloted = False
			self.release = False
			subject = "StudentsEarn - We have released your ID."
			message = f"Hello {self.user.username}, \nWe have released your ID."
			
			from_email = settings.EMAIL_HOST_USER
			recipient_list = [self.user.email, ]
			self.user = None
			
			send_mail(subject, message, from_email, recipient_list)
		super(EmailID, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.Email} - {self.is_alloted}'



class AssignRequest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	id_alloted = models.ForeignKey(EmailID, on_delete=models.CASCADE, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		print("inti")
		print(self.id_alloted)
		if self.id_alloted:
			print("saving init()...")
			temp = EmailID.objects.filter(Email=self.id_alloted.Email)
			pro = Profile.objects.filter(user=self.user)
			if (len(temp) > 0):
				temp = temp[0]
			if (len(pro) > 0):
				pro = pro[0]
			pro.id_alloted = self.id_alloted
			pro.save()
			temp.user = self.user
			temp.is_alloted = True
			temp.save()
			subject = "StudentsEarn - You have been alloted an ID."
			# message = "Hello"
			message = loader.render_to_string('core/activation_mail.html')
			print("message = ", message)
			from_email = settings.EMAIL_HOST_USER
			recipient_list = [self.user.email, ]
			send_mail(subject, message, from_email, recipient_list, fail_silently=True)
		super(AssignRequest, self).save(*args, **kwargs)

	def __str__(self):
		return self.user.username


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
	account_holder_name = models.CharField(max_length=100, default='...ABCD')
	bank_account = models.CharField(max_length=100, default='...00')
	ifsc_code = models.CharField(max_length=100, default='...ABCD')
	upi = models.CharField(max_length=100, default='..optional')
	balance = models.IntegerField(default=0)
	questions_this_month = models.IntegerField(default=0)
	id_alloted = models.ForeignKey(EmailID, on_delete=models.CASCADE, null=True, blank=True)
	subject_choice = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	is_active = models.BooleanField(default=False)
	mobile_number = models.CharField(max_length=13, null=True, blank=True)
	rank = models.CharField(max_length=5, null=True, blank=True, verbose_name="JEE/GATE Rank")
	result_file = models.ImageField(upload_to='files', null=True, blank=True, verbose_name="Upload Result")
	send_verify_mail_yes = models.BooleanField(default=False)
	send_verify_mail_no = models.BooleanField(default=False)
	subject_message = models.CharField(max_length=200, default='StudentsEarn...')
	message = models.TextField(default='Hello........')
	send_message = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Profiles"
		ordering = ['-questions_this_month',]

	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		if self.send_message:
			subject = self.subject_message
			message = self.message
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [self.user.email,]
			send_mail(subject, message, email_from, recipient_list)
		if self.send_verify_mail_yes:
			subject = "StudentsEarn - VERIFIED"
			message = loader.render_to_string('core/verify.html')
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [self.user.email,]
			send_mail(subject, message, email_from, recipient_list)
		elif self.send_verify_mail_no:
			subject = "StudentsEarn - VERIFIED"
			message = f"Hello {self.user.username},\n Sorry, You are not verified. Thank you."
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [self.user.email]
			send_mail(subject, message, email_from, recipient_list)
		self.send_verify_mail_no = False
		self.send_verify_mail_yes = False
		self.send_message = False
		super(Profile, self).save(*args, **kwargs)


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
