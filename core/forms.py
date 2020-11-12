from django.forms import ModelForm
from .models import Profile

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['account_holder_name', 'bank_account', 'ifsc_code', 'upi', 'subject_choice', 'mobile_number', 'rank', 'result_file']


class MobileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['mobile_number', ]



class QuestionForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['questions_this_month',]