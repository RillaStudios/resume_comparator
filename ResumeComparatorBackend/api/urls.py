from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from api.views.job_posting_view import JobPostingView
from api.views.compare_report_view import CompareReportView

urlpatterns = [
    path('reports/', CompareReportView.as_view(), name='reports'),
    path('reports/<int:uid>/', CompareReportView.as_view(), name='reports'),
    path('compare/', CompareReportView.as_view(), name='reports'),
    path('job-postings/', JobPostingView.as_view(), name='all-job-postings'),
    path('job-postings/<int:uid>/', JobPostingView.as_view(), name='job-postings')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)