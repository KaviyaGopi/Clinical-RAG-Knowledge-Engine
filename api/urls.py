from django.urls import path
from api.views import UploadNoteView, AskQuestionView

urlpatterns = [
    path('upload/', UploadNoteView.as_view(), name='upload_note'),
    path('ask/', AskQuestionView.as_view(), name='ask_question'),
]