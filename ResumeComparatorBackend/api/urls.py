from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from api.views.compare_view import CompareView
from api.views.job_posting_view import JobPostingView
from api.views.report_view import ReportView

urlpatterns = [
    path('reports/', ReportView.as_view(), name='reports'),
    path('reports/<int:uid>/', ReportView.as_view(), name='reports'),
    path('job-postings/', JobPostingView.as_view(), name='all-job-postings'),
    path('job-postings/<int:uid>/', JobPostingView.as_view(), name='job-postings'),
    path('compare/', CompareView.as_view(), name='compare')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)