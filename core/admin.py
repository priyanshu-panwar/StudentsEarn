from django.contrib import admin
from .models import EmailID, Category, Profile, Transaction

class TransactionInline(admin.TabularInline):
	model = Transaction
	can_delete = False
	readonly_fields = ('date',)
	extra = 1

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('user', 'credit', 'date')
	list_filter = ('user', 'date')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'upi', 'is_active', 'id_alloted', 'subject', 'questions_this_month', 'balance')
	inlines = [TransactionInline]

"""
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'is_active', 'id_alloted', 'subject')
	list_filter = ('id_alloted', 'subject')
"""
@admin.register(EmailID)
class EmailIDAdmin(admin.ModelAdmin):
	list_display = ('Email', 'Subject', 'is_alloted')

admin.site.register(Category)