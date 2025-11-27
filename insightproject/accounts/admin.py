from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'transaction_type', 'timestamp')
    search_fields = ('sender__username', 'receiver__username')
    readonly_fields = ('timestamp',)
    list_filter = ('transaction_type', 'timestamp')
