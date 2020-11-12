from django.contrib import admin
from .models import EmailID, SendMessage, Category, Profile, Transaction, Message, AssignRequest

@admin.register(SendMessage)
class SendMessageAdmin(admin.ModelAdmin):
	list_display = ('subject', 'assigned_users', 'non_assigned_users', 'all_active')

@admin.register(AssignRequest)
class AssignRequestAdmin(admin.ModelAdmin):
	list_display = ('user', 'id_alloted', 'date')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('user', 'date')
	list_filter = ('date',)

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
	list_display = ('user', 'bank_account', 'ifsc_code', 'is_active', 'id_alloted', 'subject_choice', 'questions_this_month', 'balance')
	inlines = [TransactionInline]
	search_fields = ('user__username', )

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