#coding:utf-8
from django import forms
from django.contrib.auth.models import User
# from django.conf import settings
# from django.db.models import Q
# from models import User
# import re

class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})



    # def clean(self):  
          
    #      # 用户名  
    #     try:            
    #         username=self.cleaned_data['username']  
    #     except Exception as e:  
    #         print 'except: '+ str(e)  
    #         raise forms.ValidationError(u"注册账号需为邮箱格式")      
  
  
    #     # 登录验证          
    #     is_email_exist = UserProfile.objects.filter(email=username).exists()   
    #     is_username_exist = UserProfile.objects.filter(username=username).exists()   
    #     if is_username_exist or is_email_exist:  
    #         raise forms.ValidationError(u"该账号已被注册")  
  
  
    #     # 密码  
    #     try:  
    #         password=self.cleaned_data['password']  
    #     except Exception as e:  
    #         print 'except: '+ str(e)  
    #         raise forms.ValidationError(u"请输入至少8位密码");  
  
  
    #     return self.cleaned_data    




class RegForm(forms.Form):
    '''
    注册表单
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "email不能为空",})
    url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Url", }),
                              max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

    def clean(self):  
        print 'clean'
         # 用户名  
        try:            
            username=self.cleaned_data['username']  
        except Exception as e:  
            print 'except: '+ str(e)  
            raise forms.ValidationError(u"注册账号需为邮箱格式")      
  
  
        # 登录验证          
        is_email_exist = User.objects.filter(email=username).exists()   
        is_username_exist = User.objects.filter(username=username).exists()   
        if is_username_exist or is_email_exist:
            print 'is_exist'
            raise forms.ValidationError(u"该账号已被注册")  
  
  
        # 密码  
        try:  
            password=self.cleaned_data['password']  
        except Exception as e:  
            print 'except: '+ str(e)  
            raise forms.ValidationError(u"请输入至少8位密码");  
  
  
        return self.cleaned_data    


class CommentForm(forms.Form):
    # author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
    #                                                        "required": "required","size": "25", "tabindex": "1"}),
    #                           max_length=50,error_messages={"required":"username不能为空",})
    # email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
    #                                                        "required":"required","size":"25", "tabindex":"2"}),
    #                              max_length=50, error_messages={"required":"email不能为空",})
    # url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
                                                       # "size":"25", "tabindex":"3"}),
                              # max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"commentc","class": "message_inputc",
                                                           "required": "required", "cols": "25",
                                                           "rows": "1", "tabindex": "4"}),
                                                    error_messages={"required":"评论不能为空",})
    article = forms.CharField(widget=forms.HiddenInput())
    # father = forms.CharField(widget=forms.HiddenInput())


class HuifuForm(forms.Form):
    # comment = forms.CharField(widget=forms.Textarea(attrs={"id":"huifu","class": "huifu_input",
    #                                                        "required": "required", "cols": "25",
    #                                                        "rows": "5", "tabindex": "4"}),
    #                                                 error_messages={"required":"评论不能为空",})

    article = forms.CharField(widget=forms.HiddenInput(attrs={'class':'articleid'}))
    # father = forms.CharField(widget=forms.HiddenInput())

    huifu = forms.CharField(widget=forms.Textarea(attrs={'name':'username', 'class':'hf',\
                'required':'required','onfocus':'myOnfocus(this);','onblur':'myOnblur(this)'}),
                  error_messages={"required":"评论不能为空",})
    pid = forms.CharField(widget=forms.HiddenInput(attrs={'name':'pid','class':'testpid'}))



