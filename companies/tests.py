import json
from django.test      import TestCase, Client

from companies.models import Company, CompanyName, CompanyTag, LanguageType, Tag, TagName

class CompanyTest(TestCase):
    def setUp(self):
        tag_list = [
            Tag(id = 4),
            Tag(id = 20),
            Tag(id = 16)
        ]

        Tag.objects.bulk_create(tag_list)

        language_list = [
            LanguageType(
                id   =  1,
                type = 'ko'
            ),
            LanguageType(
                id   = 2,
                type = 'en'
            ),
            LanguageType(
                id  =  3,
                type = 'ja'
            )
        ]
        
        LanguageType.objects.bulk_create(language_list)

        tag_names = [
            TagName(
                id               = 1,
                language_type_id = 1,
                tag_id           = 4,
                name             = '태그_4'
            ),
            TagName(
                id               = 2,
                language_type_id = 1,
                tag_id           = 20,
                name             = '태그_20'
            ),
            TagName(
                id               = 3,
                language_type_id = 1,
                tag_id           = 16,
                name             = '태그_16'
            )
        ]

        TagName.objects.bulk_create(tag_names)

        company_list = [
            Company(id = 1),
            Company(id = 2),
            Company(id = 3)
        ]

        Company.objects.bulk_create(company_list)

        company_name_list = [
            CompanyName(
                id               = 1,
                company_id       = 1,
                language_type_id = 1,
                name             = "주식회사 링크드코리아"
            ),
            CompanyName(
                id               = 2,
                company_id       = 2,
                language_type_id = 1,
                name             = "스피링크"
            ),
            CompanyName(
                id               = 3,
                company_id       = 3,
                language_type_id = 1,
                name             = "원티드랩"
            ),
            CompanyName(
                id               = 4,
                company_id       = 3,
                language_type_id = 2,
                name             = "wantedlab"
            )
        ]

        CompanyName.objects.bulk_create(company_name_list)

        company_tag_list = [
            CompanyTag(
                id         = 1,
                company_id = 3,
                tag_id     = 4
            ),
            CompanyTag(
                id         = 2,
                company_id = 3,
                tag_id     = 20
            ),
            CompanyTag(
                id         = 3,
                company_id = 3,
                tag_id     = 16
            )
        ]

        CompanyTag.objects.bulk_create(company_tag_list)

        global headers1, headers2, headers3
        headers1 = {'HTTP_x_wanted_language' : 'ko'}
        headers2 = {'HTTP_x_wanted_language' : 'tw'}
        headers3 = {'HTTP_x_wanted_language' : 'abc'}

    def tearDown(self):
        Tag.objects.all().delete()
        LanguageType.objects.all().delete()
        TagName.objects.all().delete()
        Company.objects.all().delete()
        CompanyName.objects.all().delete()

    def test_success_company_name_autocomplete(self):
        client   = Client()
        response = client.get("/search?query=링크", **headers1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {'data' : [
                {"company_name" : "주식회사 링크드코리아"},
                {"company_name" : "스피링크"}
                ]
            }
        )
    
    def test_success_post_company(self):
        client = Client()
        data   = {
            "company_name": {
                "ko": "라인 프레쉬",
                "tw": "LINE FRESH",
                "en": "LINE FRESH",
            },
            "tags": [
                {
                    "tag_name": {
                        "ko": "태그_1",
                        "tw": "tag_1",
                        "en": "tag_1",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_8",
                        "tw": "tag_8",
                        "en": "tag_8",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_15",
                        "tw": "tag_15",
                        "en": "tag_15",
                    }
                }
            ]
        }

        response = client.post("/companies", json.dumps(data), content_type = 'application/json', **headers2)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "data" : {
                "company_name" : "LINE FRESH",
                "tags": [
                    "tag_1",
                    "tag_8",
                    "tag_15",
                ]
            }    
        })

    def test_success_get_company_detail(self):
        client   = Client()
        response = client.get("/companies/wantedlab", **headers1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "data" : {
                "company_name" : "원티드랩",
                "tags" : [
                    "태그_4",
                    "태그_20",
                    "태그_16"
                ]
            }
        })
    
    def test_fail_company_name_autocomplete_languagetype_does_not_exist(self):
        client   = Client()
        response = client.get("/search?query=링크", **headers2)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 
            {'message' : 'LANGUAGE_TYPE_DOES_NOT_EXIST'}
        )

    def test_fail_post_company_json_decode_error(self):
        client = Client()

        response = client.post("/companies", **headers2)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message" : 'JSON_DECODE_ERROR'    
        })
    
    def test_fail_post_company_languagetype_does_not_exist(self):
        client = Client()
        data   = {
            "company_name": {
                "ko": "라인 프레쉬",
                "tw": "LINE FRESH",
                "en": "LINE FRESH",
            },
            "tags": [
                {
                    "tag_name": {
                        "ko": "태그_1",
                        "tw": "tag_1",
                        "en": "tag_1",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_8",
                        "tw": "tag_8",
                        "en": "tag_8",
                    }
                },
                {
                    "tag_name": {
                        "ko": "태그_15",
                        "tw": "tag_15",
                        "en": "tag_15",
                    }
                }
            ]
        }

        response = client.post("/companies", json.dumps(data), content_type = 'application/json', **headers3)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message" : "LANGUAGE_TYPE_DOES_NOT_EXIST"   
        })

    def test_fail_get_company_detail_company_name_does_not_exist(self):
        client   = Client()
        response = client.get("/companies/hihi", **headers1)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message" : 'COMPANY_DOES_NOT_EXIST'
        })

    def test_fail_get_company_detail_company_name_does_not_exist(self):
        client   = Client()
        response = client.get("/companies/wantedlab", **headers2)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message" : "LANGUAGE_TYPE_DOES_NOT_EXIST"
        })
    