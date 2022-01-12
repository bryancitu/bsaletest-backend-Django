# Documentation About BSALETEST backend project

I recommend visiting my website, where you will learn a little about the Django framework

[http://www.bryancinux.com/django/primeros-pasos/](http://www.bryancinux.com/django/primeros-pasos/)

### Follow the next steps to create this project

1. Create a virtual environment
```bash
~$ mkvirtualenv environment_name
```
2. Install Django
```bash
(environment_name) ~$ pip3 install django
```
3. Create project
```bash
(environment_name) ~$ django-admin startproject bsaletest
```
4.Personalization config in:
> bsaletest/settings.py

```python

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True

```
5. Install `djangorestframework` and `django-cors-headers` for RESTAPI:
```bash
(environment_name) ~$ pip3 install djangorestframework
(environment_name) ~$ pip3 install django-cors-headers
```


6. ADD apps in bsaletest/settings.py:
```python

INSTALLED_APPS = [
    ....

    # external apps
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    ...
]

#config rest framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```
7. Create our app and models(Category and Product)
```bash
(environment_name) ~$ django-admin startapp products
```
in products/models.py
```python
from django.db import models

# Create your models here.
class Category(models.Model):
    """Model definition for category."""

    name    = models.CharField('name', max_length=200)

    class Meta:
        """Meta definition for category."""

        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """Unicode representation of category."""
        return self.name

class Product(models.Model):
    """Model definition for product."""

    name        = models.CharField('name', max_length=200)
    url_image   = models.CharField('url_image', max_length=1000)
    price       = models.FloatField()
    discount    = models.IntegerField()
    category    = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        """Meta definition for product."""

        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        """Unicode representation of product."""
        return self.name
```
8. Make migrations to project (create tables in DB)
```bash
(environment_name) ~$ python3 manage.py makemigrations
(environment_name) ~$ python3 manage.py migrate
```
### NOTE: 
> En este proyecto hago uso de postgres y no de MySQL, la razon es que Django tiene una configuracion especial al crear las tablas, por lo que opte por descargarme la DB de ambas tablas  en formato csv para luego subirlo por codigo a la DB, con la cual hice uso de la libreria pandas, puede hacer uso de MySQL tambien con su configuracion de Django, pero como lo iba a asubir a Heroku automaticamente me crea una DB de postgres por eso use esa DB

9. Deploy mi data to DB:
- Open the console and  write this:
```bash
(environment_name) ~$ python3 manage.py shell
>>>|
```
- Copy the code from the deploydb.py file in the console \
`category.csv` and  `product.csv` filesare in the base path of project
```python

from products.models import *
import pandas as pd

# upload category model
df=pd.read_csv('category.csv')
id=list(df['id'])
n=list(df['name'])

for i in range(len(id)):
    Category.objects.create(
        id=id[i],
        name=n[i]
    )

# upload product model
df2=pd.read_csv('product.csv')

id2=list(df2['id'])
n2=list(df2['name'])
u=list(df2['url_image'])
p=list(df2['price'])
d=list(df2['discount'])
c=list(df2['category'])

for i in range(len(id2)):
    Product.objects.create(
        id=id2[i],
        name=n2[i],
        url_image=u[i],
        price=p[i],
        discount=d[i],
        category=Category.objects.filter(id=c[i]).first()
    )

```

- Well we have our DB with data and ready to create endpoints

10. Create our endpoints
- In `products/serializers.py`, `products/views.py`, and `products/urls.py` write code to create endpoints

11. Config for AWS S3, becouse heroku not support statics files
- Install following libraries
```bash
(environment_name) ~$ pip3 install boto3
(environment_name) ~$ pip3 install botocore
```
- in settings.py add code 
```python

STATIC_URL = '/static/'

# dir our media file
STATIC_ROOT = BASE_DIR / 'media'

# AWS_SETTINGS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'my-storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_LOCATION = 'media'
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATIC_URL = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.sa-east-1.amazonaws.com/media/'
AWS_DEFAULT_ACL = "public-read"
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}


# dir our static file (Django files by default)
STATICFILES_DIRS = [BASE_DIR / 'static']
```
12. Deploy our static files in AWS S3:
```bash
(environment_name) ~$ python3 manage.py collectstatic
```
13 Config to deploy heroku
- Install dependencies 
```bash
(environment_name) ~$ pip3 install gunicorn
(environment_name) ~$ pip3 install psycopg2-binary
(environment_name) ~$ pip3 install dj-database-url
```
- Create Procfile file and add this
```
web: gunicorn bsaletest.wsgi --log-file -
```
- Finally deploy to heroku our code with gitand our backend is ready

## Extra Notes
you can see the endpoints in the followings links
- products by category endpoint: \
general endpoint: [https://bsaletest-app.herokuapp.com/api/product/products/<<category>>/](https://bsaletest-app.herokuapp.com/api/product/products/<category>/)\
example endpoint: [https://bsaletest-app.herokuapp.com/api/product/products/pisco/](https://bsaletest-app.herokuapp.com/api/product/products/pisco/)

- category endpoint: \
[https://bsaletest-app.herokuapp.com/api/product/categories/](https://bsaletest-app.herokuapp.com/api/product/categories/)

- search enpoint: \
general endpoint: [https://bsaletest-app.herokuapp.com/api/product/search/<<query>>/](https://bsaletest-app.herokuapp.com/api/product/search/pisco/)\
example endpoint: [https://bsaletest-app.herokuapp.com/api/product/search/pisco/](https://bsaletest-app.herokuapp.com/api/product/search/pisco/)

### Django has a admin panel and the url is:

`There you can interative wit DB `

[https://bsaletest-app.herokuapp.com/admin/](https://bsaletest-app.herokuapp.com/admin/)
- Credencial for this admin is: \
 username: admin\
 password: admin

- for example after login you can go this url:\
[https://bsaletest-app.herokuapp.com/admin/products/product/](https://bsaletest-app.herokuapp.com/admin/products/product/) 
