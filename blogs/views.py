from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, InvalidPage
# Create your views here.

def index(request):
    categories = Category.objects.all()
    blogs = Blogs.objects.all()
    lastest = Blogs.objects.all().order_by('-pk')[:4]

    #บทความยอดนิยม
    popular = Blogs.objects.all().order_by('-views')[:3]

    #บทความแนะนำ
    suggestion = Blogs.objects.all().order_by('views')[:3]

    #pagination
    paginator =  Paginator(blogs,3)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        blogperpage = paginator.page(page)
    except(EmptyPage,InvalidPage):
        blogperpage = paginator.page(paginator.num_pages)
    return render(request,'frontend/index.html',
    {'categories':categories,
    'blogs':blogperpage,
    'lastest':lastest,
    'popular':popular,
    'suggestion':suggestion,
    })

def blogDetail(request,id):
    categories = Category.objects.all()
    popular = Blogs.objects.all().order_by('-views')[:3]
    suggestion = Blogs.objects.all().order_by('views')[:3]

    singleblog = Blogs.objects.get(id=id)
    singleblog.views += 1
    singleblog.save()
    return render(request,'frontend/blogDetail.html',{
        'blog':singleblog,
        'categories':categories,
        'popular':popular,
        'suggestion':suggestion,
        })

def searchCategory(request,category_id):
    blogs = Blogs.objects.filter(category_id=category_id)
    popular = Blogs.objects.all().order_by('-views')[:3]
    suggestion = Blogs.objects.all().order_by('views')[:3]
    categories = Category.objects.all()

    category_name = Category.objects.get(id=category_id)
    return render(request,'frontend/searchCategory.html',{
        'blogs':blogs,
        'popular':popular,
        'suggestion':suggestion,
        'category_name':category_name,
        'categories':categories,
        })

def searchWriter(request,writer):
    blogs = Blogs.objects.filter(writer=writer)
    popular = Blogs.objects.all().order_by('-views')[:3]
    suggestion = Blogs.objects.all().order_by('views')[:3]
    categories = Category.objects.all()

    
    return render(request,'frontend/searchWriter.html',
    {'blogs':blogs,
    'popular':popular,
    'suggestion':suggestion,
    'categories':categories,
    'writer':writer
    }
    )
    