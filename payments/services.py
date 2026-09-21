import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(course):
    """Создание продукта в Stripe."""
    if course.stripe_product_id:
        return course.stripe_product_id

    product = stripe.Product.create(
        name=course.title,
    )

    course.stripe_product_id = product.id
    course.save(update_fields=['stripe_product_id'])

    return product.id


def create_price(course):
    """Создание цены для продукта Stripe."""
    if course.stripe_price_id:
        return course.stripe_price_id

    product_id = create_product(course)

    price = stripe.Price.create(
        currency="usd",
        unit_amount=int(course.price * 100),  # Stripe принимает цену в центах
        product=product_id,
    )

    course.stripe_price_id = price.id
    course.save(update_fields=['stripe_price_id'])

    return price.id


def create_checkout_session(course, user, success_url, cancel_url):
    """Создание Stripe Checkout Session."""
    price_id = create_price(course)

    session = stripe.checkout.Session.create(
        mode='payment',
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            'course_id': course.id,
            'user_id': user.id,
        },
    )

    Payment.objects.create(
        user=user,
        course=course,
        session_id=session.id,
        amount=course.price,
    )

    return session
