from django.contrib import admin
from .models import *


#1 Categorys +

#2 Product +
#3 Milk  +
#4 Drinks +
#5 FullList +

#6 Cart +
#7 CartPlast +
#8 CartPaper +
#9 CartGlas +
#10 CartGeneral +
#11 CartDanger +

#12 Customer +

# total -12 models

admin.site.register(Category)

admin.site.register(Milk)
admin.site.register(Drinks)
admin.site.register(FullList)

admin.site.register(Cart)
admin.site.register(CartPlast)
admin.site.register(CartPaper)
admin.site.register(CartGlas)
admin.site.register(CartDanger)
admin.site.register(CartGeneral)
admin.site.register(CartProduct)

admin.site.register(Customer)
admin.site.register(Battery)
