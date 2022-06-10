import json


from UserApp.models import Book


class BooksListMixin:
    def get_context_data(self,**kwargs):
        context = super(BooksListMixin, self).get_context_data(**kwargs)

        context['books_json'] = json.dumps(list(Book.objects.all().values()))
        return context