import json

from UserApp.models import Book, genre_choices


def GetModelJsonData(model):
    return json.dumps(list(model.objects.values()))


class BooksJsonContextMixin:
    def get_context_data(self, **kwargs):
        context = super(BooksJsonContextMixin, self).get_context_data(**kwargs)
        context['genre_choices'] = genre_choices
        context['books_json'] = GetModelJsonData(Book)
        return context
