from django.shortcuts import render
from . models import Post

# Create your views here.


def fashion_tips(request):

    posts = Post.objects.all().order_by('-id')[:6]

    context = {
        'posts': posts,
    }

    return render(request, 'posts/fashion_tips.html', context)
