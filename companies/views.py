import json
from json.decoder         import JSONDecodeError

from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Q

from companies.models     import Company, CompanyName, TagName, LanguageType, CompanyTag

class CompanyView(View):
    def get(self, request):
        try:
            query         = request.GET.get('query')
            search_filter = Q()
            
            if query :
                search_filter.add(Q(name__icontains = query), Q.AND)
            
            language         = request.headers.get('x-wanted-language')
            language_type    = LanguageType.objects.get(type = language)
            search_companies = CompanyName.objects.select_related('company').filter(search_filter)
            company_id_list  = [company.company_id for company in search_companies]
            company_names    = CompanyName.objects.filter(company_id__in = company_id_list, language_type = language_type)
            result           = [{"company_name" : company.name } for company in company_names]

            return JsonResponse({'data' : result}, status = 200)

        except LanguageType.DoesNotExist:
            JsonResponse({'message' : "LANGUAGE_TYPE_DOES_NOT_EXIST"}, status = 404)

class CompanyDetaileView(View):
    def get(self, request, company_name):
        try:
            if not CompanyName.objects.filter(name = company_name).exists():
                return JsonResponse({'message' : 'COMPANY_DOES_NOT_EXIST'}, status = 404)

            language       = request.headers.get('x-wanted-language')
            language_type  = LanguageType.objects.get(type = language)
            search_company = CompanyName.objects.get(name = company_name)
            company        = CompanyName.objects.get(company_id = search_company.company_id, language_type = language_type)
            tags           = CompanyTag.objects.filter(company_id = search_company.company_id)
            tag_id_list    = [tag.tag_id for tag in tags]
            tag_names      = TagName.objects.filter(tag_id__in = tag_id_list, language_type = language_type)
            result         = {"company_name" : company.name,
                            "tags"         : [tag.name for tag in tag_names]
                            }

            return JsonResponse({'data' : result}, status = 200)

        except LanguageType.DoesNotExist:
            return JsonResponse({'message' : "LANGUAGE_TYPE_DOES_NOT_EXIST"}, status = 404)
        
        except CompanyName.DoesNotExist:
            return JsonResponse({'message' : "COMPANY_DOES_NOT_EXIST"}, status = 404)

            

