from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import (
    Q,
    F,
    Count,
    Max,
    Case,
    When,
    Value,
    BooleanField,
    Func,
    DecimalField,
    ExpressionWrapper,
)
from django.db import transaction, connection
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType

from store.models import Product, Customer, Address, OrderItem, Order, Collection
from tags.models import TaggedItem


# Create your views here.
def say_hello(request):
    # result = Customer.objects.annotate(
    #     full_name=Func(F("first_name"), Value(" "), F("last_name"), function="CONCAT")
    # )

    # result = Customer.objects.annotate(
    #     orders=Count('order'),
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # ).order_by('-orders')

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField)
    # products = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )

    # content_type = ContentType.objects.get_for_model(Product)

    # query_set = TaggedItem.objects \
    # .select_related("tag") \
    # .filter(
    #     content_type=content_type,
    #     object_id=1
    # )

    # collection = Collection(pk=51, title='Game Videos Update', featured_product_id=10)
    # # collection.title = 'Game Videos'
    # collection.featured_product_id = 2
    # collection.save()

    # collection = Collection.objects.filter(pk=51).update(featured_product=1)

    # print(collection.id)

    # transaction.atomic()

    # collection = OrderItem.objects.filter(id__lt=10).delete()

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     orderItem = OrderItem()
    #     orderItem.order = order
    #     orderItem.product_id = 1
    #     orderItem.unit_price = 10
    #     orderItem.quantiy = 12
    #     orderItem.save()

    # queryset = Product.objects.raw("SELECT id, title FROM store_product;")
    # # print(queryset[0].title)
    # # print(list(queryset))

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT id, title FROM store_product;")
    #     rows = cursor.fetchall()
    #     cursor.close()

    # # print(list(rows))
    # rows = [{"id": row[0], "title": row[1]} for row in rows]






    return render(request, "hello.html", {"products": None})
