from django.contrib import admin
from .models import product, Review, Report, Category, Payout, LedgerEntry


# Register your models here.
admin.site.register(product)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'created')
    list_filter = ('rating',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reason', 'status', 'product', 'seller', 'reporter', 'created')
    list_filter = ('status', 'reason')
    actions = ['mark_resolved', 'mark_dismissed']

    @admin.action(description='Mark selected reports as resolved')
    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved')

    @admin.action(description='Mark selected reports as dismissed')
    def mark_dismissed(self, request, queryset):
        queryset.update(status='dismissed')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name_en', 'name_ar')
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'amount', 'status', 'created', 'paid_at')
    list_filter = ('status',)


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'kind', 'amount', 'order', 'created')
    list_filter = ('kind',)
