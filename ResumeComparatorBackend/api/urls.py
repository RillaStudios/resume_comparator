from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from api.models.compare_report_resume_download import CompareReportResumeDownload
from api.views.job_posting_view import JobPostingView
from api.views.compare_report_view import CompareReportView
from api.views.user_view import register, login, logout, view_profile, update_profile, delete_user, change_password, protected_view

urlpatterns = [
    path('reports/', CompareReportView.as_view(), name='reports'),
    path('reports/<int:uid>/', CompareReportView.as_view(), name='reports'),
    path('compare/', CompareReportView.as_view(), name='reports'),
    path('job-postings/', JobPostingView.as_view(), name='all-job-postings'),
    path('job-postings/<int:uid>/', JobPostingView.as_view(), name='job-postings'),
    path('reports/download/', CompareReportResumeDownload.as_view(), name='download-resumes'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', view_profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/delete/', delete_user, name='delete_user'),
    path('profile/changepass/', change_password, name='change_password'),
    path('protected/', protected_view, name='protected_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)