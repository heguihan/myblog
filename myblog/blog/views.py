#coding:utf-8
from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
import logging
from django.conf import settings
from models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Count
from forms import *
from django.contrib import auth
# Create your views here.
# logger = logging.getLogger('blog.views')


def globle_setting(request):
	# pass

    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # coment_count = Comment.objects.value('article').annotate(com_count=Count('article'))

    # #commen_counts = Comment.objects.value('article').annotate(com_count=Count('article')).order_by('-com_count')
    # comment_article_list = [Article.objects.GET.get(pk=com['article']) for com in comment_count]
    archive_list = Article.objects.distinct_date()
    tag_list = Tag.objects.all()
    commen_counts = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    
    browse_article_list_all = Article.objects.order_by('-click_count')
    recommended_article_list_all = Article.objects.filter(is_recommend=True)
    comment_article_list_all = [Article.objects.get(pk=comment_article['article']) for comment_article in commen_counts]
    #截取前5个
    browse_article_list = browse_article_list_all[0:5] if(len(browse_article_list_all)>5)else browse_article_list_all
    recommended_article_list = recommended_article_list_all[0:5] if(len(recommended_article_list_all)>5)else recommended_article_list_all
    comment_article_list = comment_article_list_all[0:5] if(len(comment_article_list_all)>5)else comment_article_list_all


    return locals()



def test(request):
    article_list = Article.objects.all()
    commen_counts = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    comment_article_test_list = [Article.objects.get(pk=com['article']) for com in commen_counts]

    browse_article_list = Article.objects.order_by('-click_count')
    recommended_article_list = Article.objects.filter(is_recommend=True)
    


    return render(request, 'testExit.html', locals())

def index(request):
    try:
        # comment_counts = Article.objects.annotate(num_comment=count('Comment'))
        article_list = Article.objects.all()
        # commen_counts = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
        # comment_article_list = [Article.objects.get(pk=comment_article['article']) for comment_article in commen_counts]

        # browse_article_list = Article.objects.order_by('-click_count')
        # recommended_article_list = Article.objects.filter(is_recommend=True)

        # archive_list = Article.objects.distinct_date()
        

        print 'blog+++++++++++++++'
        name = request.user.username
        print name

        paginator = Paginator(article_list, 2)

        try:
            page = int(request.GET.get('page', 1))
            article_list = paginator.page(page)

        except(EmptyPage, PageNotAnInteger, InvalidPage):
            article_list = paginator.page(1)

    except Exception as e:
        # logger.error(e)
        pass




	# try:
 #        article_list = Article.objects.all()
 #        totle_page = 'ssskkk'
 #        paginator = Paginator(article_list, 2)
 #        try:
 #            page = int(request.GET.get('page', 1))
 #            article_list = paginator.page(page)
 #            current_page = page
 #            totle_page = article_list.count()
 #        except(EmptyPage, PageNotAnInteger, InvalidPage):
 #            article_list = paginator.page(1)
	# except Exception as e:
	# 	print e
	# # 	logger.error(e)
 #    try:
 #        article_list = Article.objects.all()




    return render(request, 'test.html',locals())



# 文章详情

def article(request):


    # comment_form = CommentForm()
    # comment_form = CommentForm({'author': request.user.username,
    #                                 'email': request.user.email,
    #                                 'article': id} if request.user.is_authenticated() else{'article': id})


    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
            # author = article.user.username
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
        # comment_form = CommentForm({'article': id})
        huifu = HuifuForm({'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_fathor_list = []
        # for comment in comments:
        #     testuser = comment.user
        #     for item in comment_list:
        #         if not hasattr(item, 'children_comment'):
        #             setattr(item, 'children_comment', [])
        #         if comment.pid == item:
        #             item.children_comment.append(comment)
        #             break
        #     if comment.pid is None:
        #         comment_list.append(comment)
        for comment in comments:
            testuser = comment.user
            if not hasattr(comment, 'children_comment'):
                setattr(comment, 'children_comment',[])
            if not hasattr(comment, 'father_name'):
                setattr(comment, 'father_name','')
            if comment.pid is None:
                comment_fathor_list.append(comment)
            else:

                getusername = comment.pid.user.username
                comment.father_name = getusername


            for father_comment in comment_fathor_list:
                # return render(request, 'testceshi.html')
                if comment.pid:



                    while comment.pid not in comment_fathor_list:
                        f = comment.pid
                        comment.pid = f.pid


                if comment.pid == father_comment:
                    father_comment.children_comment.append(comment)
                    # return render(request, 'testceshi.html')
    except Exception as e:
        print e
        # return render(request, 'testceshi.html')
        return render(request, 'testfailure.html', {'e': e})
        # logger.error(e)
    return render(request, 'article.html', locals())


def archive(request):
    try:
        archive_list = Article.objects.distinct_date()
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        paginator = Paginator(article_list, 2)
        
        # print '哈哈卡扩扩扩扩扩所扩所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所所'
        # for ar in archive_list:
        #     print ar
        try:
            page = int(request.GET.get('page', 1))
            article_list = paginator.page(page)
            current_page = page
            totle_page = article_list.count()
        except(EmptyPage, PageNotAnInteger, InvalidPage):
            article_list = paginator.page(1)
    except Exception as e:
        # logger.error(e)
        pass

    return render(request, 'archive.html', locals())

def tag(request):
    
    tagid = request.GET.get('id', None)
    tag = Tag.objects.filter(id=tagid)
    article_list = Article.objects.filter(tag=tagid)
    for t in tag:
        print t.name
    print '=============='
    # print tag.name
    return render(request, 'tag.html',locals())
        # return HttpResponse('tag.name')

    # return render(request, 'tag.html')




    # return HttpResponse('archive')


# def comment_post(request):
#     # return HttpResponse('comment_post')
#     try:
#         # comment_form = CommentForm(request.POST)
#         request.method == 'POST'
#         # logger.error('sss')
#         if comment_form.is_valid():
#             #获取表单信息
#             comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
#                                              email=comment_form.cleaned_data["email"],
#                                              url=comment_form.cleaned_data["url"],
#                                              content=comment_form.cleaned_data["comment"],
#                                              article_id=comment_form.cleaned_data["article"],
#                                              user=request.user if request.user.is_authenticated() else None)
#             comment.save()
#         else:
#             return render(request, 'failure.html', {'reason': comment_form.errors})
#     except Exception as e:
#         logger.error(e)
#         pass
#     return redirect(request.META['HTTP_REFERER'])

def comment_post(request):
    # return HttpResponse('comment_post')

    print '*************中文中文中文中文*********'
         # 评论表单
    comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'article': id} if request.user.is_authenticated() else{'article': id})

        # return HttpResponse('yes')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        # logger.error('sss')
        if comment_form.is_valid():
            #获取表单信息

            ar = comment_form.cleaned_data['article']
            print '============================='
            print type(ar)
            print ar
            # return HttpResponse('ok')
            comment = Comment.objects.create(
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})

        return redirect(request.META['HTTP_REFERER'])

def commentgo(request):
    comment_form = CommentForm()
    return render(request, 'testfailure.html', {'e': 'ok'})



def do_logout(request):
    auth.logout(request)
    return redirect('/blog')

# def do_reg(request):
#     return HttpResponse('do_reg')

# def do_login(request):
#     return HttpResponse('do_login')

def login(request):
    # return HttpResponse('login')
    error_log = ''
    log_form = LoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print '$$$$$$$$$$$$$$$'
        print username
        print password

        user = auth.authenticate(username = username, password = password)
        if user:
            auth.login(request,user)
            response = redirect('/blog')
            response.set_cookie('username',username,3600)
            return response
        else:
            print 'error'
            error_log = '用户名或密码错误'
            # setFormTips(reg_form, "注册失败，请重试")  


    return render(request, 'login.html', locals())

def register(request):
    # return HttpResponse('register')

    reg_form = RegForm()
    print 'register'

    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        print 'post'

        if reg_form.is_valid():
            name = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            url = reg_form.cleaned_data['url']
            password = reg_form.cleaned_data['password']

            print '====================='
            print name
            print email
            print url
            print password

            # user_blog = User.objects.create(
            #     username = name,
            #     password = password,
            #     email = email,
            #     # qq = url,
            #     # mobile = url
            #     )
            user_blog = User()
            user_blog.username = name
            user_blog.set_password(password)
            user_blog.email = email
            is_active = True
            user_blog.save()
            user_blog.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式  
                # 验证成功登录  
            auth.login(request, user_blog) 


            return redirect('/blog')

        else:
            print 'is not valid'




    return render(request,'reg.html',locals())


def category(request):
    id = request.GET.get('cid', None)
    return HttpResponse('category')


def huifu(request):

    print '================回复======================'
    print id
    # com_form = HuifuForm({'acticle':id})
    # article = com_form['article']
    # return render(request, 'testcomment.html', locals())
    if request.method == 'POST':
        com_form = HuifuForm(request.POST)
        
        if com_form.is_valid():

            print '**************is_valid成功******************'
            com =com_form.cleaned_data['huifu']
            pid = com_form.cleaned_data['pid']
            article = com_form.cleaned_data['article']
            comment = Comment.objects.create(
                content = com_form.cleaned_data['huifu'],
                article_id = com_form.cleaned_data['article'],
                pid_id = com_form.cleaned_data['pid'],
                user = request.user if request.user.is_authenticated() else None                
                )
            comment.save()

            # return render(request, 'testcomment.html', locals())
        else:
            return render(request, 'testceshi.html')



    # huifu = HuifuForm()
    # return HttpResponse('huifu')
    # return render(request, 'article.html')
    return redirect(request.META['HTTP_REFERER'])
    # return HttpResponse('huifu')
