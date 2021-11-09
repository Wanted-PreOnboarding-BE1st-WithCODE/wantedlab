from django.urls     import path,include

from companies.views import CompanyView

urlpatterns = [
    path('search', CompanyView.as_view()),
    path('companies', include('companies.urls'))
]
