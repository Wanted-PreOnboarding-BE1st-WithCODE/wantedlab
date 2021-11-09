from django.db import models

class Company(models.Model):
    pass

    class Meta:
        db_table = 'companies'

class Tag(models.Model):
    pass
    
    class Meta:
        db_table = 'tags'

class LanguageType(models.Model):
    type = models.CharField(max_length = 50, unique = True)

    class Meta:
        db_table = 'language_types'

class CompanyName(models.Model):
    company       = models.ForeignKey(Company, on_delete = models.CASCADE)
    language_type = models.ForeignKey(LanguageType, on_delete = models.CASCADE)
    name          = models.CharField(max_length = 200)
    
    class Meta:
        db_table = 'company_names'

class TagName(models.Model):
    tag           = models.ForeignKey(Tag, on_delete = models.CASCADE)
    language_type = models.ForeignKey(LanguageType, on_delete = models.CASCADE)
    name          = models.CharField(max_length = 200)
    
    class Meta:
        db_table = 'tag_names'

class CompanyTag(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    tag     = models.ForeignKey(Tag, on_delete = models.CASCADE)

    class Meta:
        db_table = 'company_tags'

