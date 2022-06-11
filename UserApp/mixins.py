import json

from UserApp.models import Book


def GetModelJsonData(model):
    return json.dumps(list(model.objects.values()))


class BooksJsonContextMixin:
    def get_context_data(self, **kwargs):
        context = super(BooksJsonContextMixin, self).get_context_data(**kwargs)

        context['books_json'] = GetModelJsonData(Book)
        return context
