
from email.mime import image
from django.contrib import messages
from django.shortcuts import redirect, render
from blogs.models import Blogs
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage

# Create your views here.
@login_required(login_url='member')
def panel(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    totalviews = Blogs.objects.filter(writer=writer).aggregate(Sum('views'))
    return render(request,'backend/index.html',{'blogs':blogs,'writer':writer,'blogCount':blogCount,'totalviews':totalviews})

@login_required(login_url='member')
def displayForm(request):
    categories = Category.objects.all()
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    totalviews = Blogs.objects.filter(writer=writer).aggregate(Sum('views'))
    return render(request,'backend/blogForm.html',{'blogs':blogs,
    'writer':writer,
    'blogCount':blogCount,
    'totalviews':totalviews,
    'categories':categories})

@login_required(login_url='member')
def insertData(request):
    try:
        if request.method == 'POST' and request.FILES['image']:
            datafile = request.FILES['image']

            #รับค่าจากฟอร์ม
            name = request.POST['name']
            category = request.POST['category']
            description = request.POST['description']
            content = request.POST['content']
            writer = auth.get_user(request)
            if str(datafile.content_type).startswith('image'):
                fs = FileSystemStorage()
                img_url = 'blogImage/'+datafile.name
                fs.save(img_url,datafile)

                #บันทึกข้อมูล
                blog = Blogs(name=name,category_id=category,description=description,content=content,writer=writer,image=img_url)
                blog.save()
                return redirect('panel')
            else:
                messages.info(request,'file type is not supported')
                return redirect('displayForm')
    except:
        return redirect('displayForm')

@login_required(login_url='member')
def deleteData(request,id):
    try:
        #ลบข้อมูล
        blog = Blogs.objects.get(id=id)
        blog.delete()
        
        #ลบภาพปกบทความ
        fs = FileSystemStorage()    
        fs.delete(str(blog.image))
        return redirect('panel')
    except:
        return redirect('panel')

@login_required(login_url='member')
def editData(request,id):
    try:
        blogEdit = Blogs.objects.get(id=id)
        categories = Category.objects.all()
        writer = auth.get_user(request)
        blogs = Blogs.objects.filter(writer=writer)
        blogCount = blogs.count()
        totalviews = Blogs.objects.filter(writer=writer).aggregate(Sum('views'))
        print(blogEdit.category.id)
        return render(request,'backend/editForm.html',{'blogEdit':blogEdit,
        'categories':categories,
        'writer':writer,
        'blogCount':blogCount,
        'totalviews':totalviews,
        })
    except:
        return redirect('panel')

@login_required(login_url='member')
def updateData(request,id):
    try:
        if request.method == 'POST':
        # ดึงข้อมูลบทความที่ต้องการแก้ไขมาใช้งาน
            blog = Blogs.objects.get(id=id)

            # รับค่าฟอร์ม
            name = request.POST['name']
            category = request.POST['category']
            description = request.POST['description']
            content = request.POST['content']

            #อัพเดทข้อมูล
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()

            #อัพเดทภาพปก 
            if request.FILES['image']:
                datafile = request.FILES['image']
                if str(datafile.content_type).startswith('image'):
                    # ลบภาพเดิมของบทความ
                    fs = FileSystemStorage()    
                    fs.delete(str(blog.image))

                    # แทนที่ภาพใหม่
                    img_url = 'blogImage/'+datafile.name
                    fs.save(img_url,datafile)
                    blog.image = img_url
                    blog.save()
            return redirect('panel')
    except:
        return redirect('panel')