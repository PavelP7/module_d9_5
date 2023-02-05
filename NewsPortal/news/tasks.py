from .models import Post, Category, User
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def periodic_mails_send():
    posts_list = {}
    last_week = datetime.now() - timedelta(weeks=1)

    for user in User.objects.all():
        for category in Category.objects.filter(subscribers=user):
            posts = list(Post.objects.filter(category=category, datetime_in__gte=last_week).values())
            if user in posts_list.keys():
                posts_list[user].append(posts)
            else:
                posts_list[user] = posts

    for user in posts_list.keys():
        html_content = render_to_string(
            'mail_form_list.html',
            {
                'username': user.username,
                'posts': posts_list[user],
            }
        )

        msg = EmailMultiAlternatives(
            subject=f"Подборка статей за прошедшую неделю",
            to=[f'{user.email}'],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

