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
