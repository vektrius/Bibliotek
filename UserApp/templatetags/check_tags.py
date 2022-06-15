from django import template

from UserApp.models import Account

register = template.Library()

@register.filter
def BookInReadListUser(user,book):
    account = Account.objects.get(user = user)
    return book in account.list_read_book.all()