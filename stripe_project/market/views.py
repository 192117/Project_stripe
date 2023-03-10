import stripe
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from stripe_project.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY

from .models import Discount, Item, Order, Tax
from .serializers import ItemSerializer


class CancelView(TemplateView):
    ''' View for URL the customer will be directed to if they decide to cancel payment and return to your website. '''
    template_name = 'cancel.html'


class SuccessView(TemplateView):
    ''' View for URL to which Stripe should send customers when payment or setup is complete. '''
    template_name = 'success.html'


class ItemDetailView(RetrieveAPIView):
    ''' View return HTML for "item/<int:id>/" '''
    model = Item
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'market/item.html'

    def get(self, request, *args, **kwargs):
        stripe_key = STRIPE_PUBLIC_KEY
        item = Item.objects.get(id=kwargs.get('id'))
        return Response({'item': item, 'stripe_key': stripe_key})


class CartDetailView(RetrieveAPIView):
    ''' View return HTML for "cart/<int:id>/" '''
    model = Order
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'market/cart.html'

    def get(self, request, *args, **kwargs):
        stripe_key = STRIPE_PUBLIC_KEY
        order = Order.objects.get(id=kwargs.get('id'))
        return Response({'order': order, 'stripe_key': stripe_key})


def buy_item(request, id, currency='usd'):
    item = Item.objects.get(id=id)
    stripe.api_key = STRIPE_SECRET_KEY
    data = {
        "name": item.name,
        "quantity": 1,
        "currency": currency,
        "amount": 0,
    }
    if currency == 'usd':
        data['amount'] = item.price_usd
    else:
        data['amount'] = item.price_eur
    checkout_session = stripe.checkout.Session.create(
        success_url='http://5.104.108.168:8000/success',
        cancel_url='http://5.104.108.168:8000/cancel',
        line_items=[
            data,
        ],
        mode="payment",
    )
    return JsonResponse({
        'id': checkout_session.id
    })


def buy_order(request, id, currency='usd'):
    order = Order.objects.get(id=id)
    disc = Discount.objects.get(order=order.id)  # last coupon
    tax = Tax.objects.get(order=order.id)  # last tax
    stripe.api_key = STRIPE_SECRET_KEY
    items = []
    if currency == 'usd':
        for item in order.items.all():
            items.append({
                "name": item.name,
                "quantity": 1,
                "currency": currency,
                "amount": item.price_usd,
                'tax_rates': [tax.stripe_tax_id]
            })
        discount = disc.stripe_usd_id
    else:
        for item in order.items.all():
            items.append({
                "name": item.name,
                "quantity": 1,
                "currency": currency,
                "amount": item.price_eur,
                'tax_rates': [tax.stripe_tax_id]
            })
        discount = disc.stripe_eur_id
    checkout_session = stripe.checkout.Session.create(
        success_url='http://5.104.108.168:8000/success',
        cancel_url='http://5.104.108.168:8000/cancel',
        line_items=items,
        mode="payment",
        discounts=[{'coupon': discount},]
    )
    return JsonResponse({
        'id': checkout_session.id
    })
