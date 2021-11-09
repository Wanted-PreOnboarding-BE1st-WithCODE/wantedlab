from django.urls     import path

from companies.views import CompanyView, CompanyDetaileView

urlpatterns = [
    path('/<str:company_name>', CompanyDetaileView.as_view()),
    path('',CompanyView.as_view())
]