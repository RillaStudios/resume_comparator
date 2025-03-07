from django.urls import path

from api.views.compare_view import CompareView
from api.views.job_posting_view import JobPostingView
from api.views.report_view import ReportsView
from api.views.reports_view import ReportView

urlpatterns = [
    path('reports/', ReportsView.as_view(), name='reports'),
    path('reports/<int:uid>/', ReportView.as_view(), name='report'),
    path('job-postings/', JobPostingView.as_view(), name='job-postings'),
    path('compare/', CompareView.as_view(), name='compare')
]