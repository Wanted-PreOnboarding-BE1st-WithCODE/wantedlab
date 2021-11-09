import json
from json.decoder         import JSONDecodeError

from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Q

from companies.models     import Company, CompanyName, Tag, TagName, LanguageType, CompanyTag

class CompanyView(View):
    def get(self, request):
        try:
            language      = request.headers.get('x-wanted-language')

            if not LanguageType.objects.filter(type = language).exists():
                return JsonResponse({'message' : 'LANGUAGE_TYPE_DOES_NOT_EXIST'}, status = 404)

            query         = request.GET.get('query')
            search_filter = Q()
            language_type = LanguageType.objects.get(type = language)
            
            if query :
                search_filter.add(Q(name__icontains = query), Q.AND)
            
            search_companies = CompanyName.objects.select_related('company').filter(search_filter)
            company_id_list  = [company.company_id for company in search_companies]
            company_names    = CompanyName.objects.filter(company_id__in = company_id_list, language_type = language_type)
            result           = [{"company_name" : company.name } for company in company_names]

            return JsonResponse({'data' : result}, status = 200)

        except LanguageType.DoesNotExist:
            JsonResponse({'message' : "LANGUAGE_TYPE_DOES_NOT_EXIST"}, status = 404)
    
    def post(self, request):
        try:
            data          = json.loads(request.body)
            language      = request.headers.get('x-wanted-language')
            company_name  = data.get('company_name')
            tag_list      = data.get('tags')
            language_list = list(company_name.keys())
            company       = Company.objects.create()

            for i in range(len(tag_list)):
                tag_id = tag_list[i]['tag_name'][language_list[0]].split('_')[1]
                
                if not Tag.objects.filter(id = tag_id).exists():
                    Tag.objects.create(id = tag_id)

                CompanyTag.objects.create(
                    company = company,
                    tag_id  = tag_id
                    )
        
            for type in language_list:
                language_type, is_language_type = LanguageType.objects.get_or_create(
                    type = type
                )
                CompanyName.objects.create(
                    company       = company,
                    language_type = language_type,
                    name          = company_name[type]
                )

                for i in range(len(tag_list)):
                    tag_id = tag_list[i]['tag_name'][type].split('_')[1]

                    TagName.objects.get_or_create(
                        tag_id        = tag_id,
                        language_type = language_type,
                        name          = tag_list[i]['tag_name'][type]
                    )
            
            if not LanguageType.objects.filter(type = language).exists():
                return JsonResponse({'message' : 'LANGUAGE_TYPE_DOES_NOT_EXIST'}, status = 404)

            language_type = LanguageType.objects.get(type = language)
            company_name  = CompanyName.objects.get(company = company, language_type = language_type)
            tags          = CompanyTag.objects.select_related('tag').filter(company = company)
            tag_id_list   = [tag.tag_id for tag in tags]
            tag_names     = TagName.objects.filter(tag_id__in = tag_id_list, language_type = language_type)
            result        = {"company_name" : company_name.name,
                             "tags"         : [tag.name for tag in tag_names]
                            }

            return JsonResponse({'data' : result}, status = 201)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)
        
        except LanguageType.DoesNotExist:
            JsonResponse({'message' : "LANGUAGE_TYPE_DOES_NOT_EXIST"}, status = 404)
        
        except CompanyName.DoesNotExist:
            return JsonResponse({'message' : "COMPANY_DOES_NOT_EXIST"}, status = 404)

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

            

