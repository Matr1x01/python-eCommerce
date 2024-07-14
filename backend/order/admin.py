from django.contrib import admin
from django import forms
from .models import Order, OrderItem
from backend.enums.DeliveryMethod import DeliveryMethod
from backend.enums.PaymentMethod import PaymentMethod
from backend.enums.status import Status
from django.utils.html import format_html


class OrderCustomForm(forms.ModelForm):
    delivery_method = forms.ChoiceField(choices=[(m.value, m.name) for m in DeliveryMethod])
    payment_method = forms.ChoiceField(choices=[(m.value, m.name) for m in PaymentMethod])

    class Meta:
        model = Order
        fields = '__all__'


class OrderAdmin(admin.ModelAdmin):
    form = OrderCustomForm

    def items(self, obj):
        section = '<ol>'
        for item in obj.items.filter(status=Status.ACTIVE.value).all():
            section += '<li><a href="/admin/order/orderitem/%s/change">%s</a></li>' % (item.id, item.product)
        section += '</ol>'

        return format_html(section)

    class Meta:
        model = Order


    readonly_fields = ('total', 'discount', 'tax', 'shipping', 'sub_total', 'total_items', 'items')


class OrderItemAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderItem

    fields = ('order', 'product', 'quantity', 'status', 'price', 'total')
    readonly_fields = ('order', 'total', 'price', 'product')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
