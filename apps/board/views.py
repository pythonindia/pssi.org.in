from datetime import datetime
from django.views.generic import ListView
from .models import BoardMember


class BoardListView(ListView):
    model = BoardMember
    template_name = 'about.html'
    context_object_name = 'board_member'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(end_date__gte=datetime.now())
