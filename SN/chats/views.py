from django.conf import settings 

from urllib.parse import quote_plus

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError, HttpResponseBadRequest

# Create your views here.

# for user signup/login
from django.contrib.auth.decorators import login_required

# for CRUD
from .forms import MessageForm, ChatUnionForm
from .models import Message, Chat, ChatUnion
from accounts.models import Profile
# fior search on list
from django.db.models import Q

# pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
from django.http import JsonResponse


# chat_union  chat_owner  chat_name created updated  get_inner_msgs last_created_msg last_updated_msg get_absolute_url get_delete_url

# from functools import reduce

@login_required
def update_msgs(request, slug):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, slug=slug)
        data = ((render(request, 'to_render_msgs.html', context={'chat_instance': chat})).__dict__.get('_container')[0]).decode("utf-8").replace("\r\n", "\n")
        return JsonResponse({'data': data})
    else:
        return HttpResponseBadRequest


@login_required
def update_chats(request):
    if request.method == 'POST':
        # own_chats = request.user.profile.own_chats.filter(deleted=False) 
        # reduced_own_chats = list(filter(lambda elem: elem.msgs_exists, own_chats))
        # chat_ids = [elem.id for elem in reduced_own_chats]
        # queryset = Chat.objects.filter(id__in=chat_ids)
        queryset = Chat.objects.sort_by_msgs(request.user)

        paginator = Paginator(queryset, 10)
        queryset = paginator.page(1)


        context = {
            "chat_list": queryset,
        }
        data = ((render(request, "sublists/main_list_chats.html", context)).__dict__.get('_container')[0]).decode("utf-8").replace("\r\n", "\n")
        return JsonResponse({'data': data})
    else:
        return HttpResponseBadRequest


# by the truth this is chat unions list
@login_required
def chat_list(request): # LIST search in chats not in mesgs
    # print(settings.ALLOWED_HOSTS)
    # search in chats by name and so on ...
    # queryset_list = ChatUnion.obje			                            cts.filter(people_in_chat__user=request.user)#| # user = user
    # Q(receivers__user=request.user)) # profile in profiles # message in witch receivers profile has us\
    # own_chats = request.user.profile.own_chats.filter(deleted=False) # all chats that wont deleted (abstractly. not actually really ) for user
    # # get queryset_list of chats that have msgs
    # reduced_own_chats = list(filter(lambda elem: elem.msgs_exists, own_chats))
    # chat_ids = [elem.id for elem in reduced_own_chats]
    # queryset_list = Chat.objects.filter(id__in=chat_ids)
    queryset_list = Chat.objects.sort_by_msgs(request.user)
    # queryset_list = [elem if elem.msgs_exists else for elem in queryset_list]
    # own_chats_ids = own_chats.values_list('id', flat=True)
    # my_chat_and_cu_list =  [[chat, chat.chat_union] for chat in own_chats] # chat, union list
    # # own_chats_ids = own_chats.values_list('id', flat=True)
    # # cus = ChatUnion.objects.filter(relative_chats__in=own_chats_ids)
    # # cus.get_related_chats(own_chats_ids)
    # # rel_chats_ids = [[own_chat_id, related_chats_id] for own_chat_id in own_chats]
    # # my_and_others_rel_chats = [[chat.chat_union] for chat in own_chats]
    # for my_chat_and_cu in my_chat_and_cu_list:
    #     for relative_chat in (my_chat_and_cu[1]).get_related_chats(my_chat_and_cu[0]):
    #         # datetime comprassion
    #         if relative_chat.last_created_msg.created >= my_chat_and_cu[0].last_created_msg.created:
                
    #         if relative_chat.last_updated_msg.updated >= my_chat_and_cu[0].last_updated_msg.updated: # new updated newer than my last updated
    # for chat in own_chats:
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(chat_name__icontains=query)|
            Q(created__icontains=query)|
            Q(slug__icontains=query)|
            Q(chat_owner__user__username__icontains=query)
            # Q(slug__last_name__icontains=query)
        ).distinct()


    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    is_paged = paginator.num_pages > 1

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "chat_list": queryset, 
        # "type": 'chat_list',
        "base_template": 'base.html',
        "page_request_var": page_request_var,
        "is_paginated": is_paged,
    }
    return render(request, "chat_list.html", context)



def chat_detail(request, slug):

    chat_instance = get_object_or_404(Chat, slug=slug)
    print('msgs\n\n')
    # [print(msg.image) for msg in chat_instance.get_inner_msgs]
    # [print(msg.image.url) for msg in chat_instance.get_inner_msgs]
    print('msgs\n\n')
    # m_form = MessageForm(request.POST or None, request.FILES or None) # send it to sub html plugged-in         chat_detail.html
    new_msgs_readed = chat_instance.read_new_messages if chat_instance.count_new_messages > 0 else False
    if new_msgs_readed is None:
        print("\nError chat.views.chat_detail\n")
    
    context = {
        "chat_instance": chat_instance,
        # "m_form": m_form,
        "theme": "Chat Detail",
        "base_template": "base.html",
    }
    return render(request, "chat_detail.html", context)

# chat_create initial ( for 1 user auto add its profile id and chat_name = profile.username ) or custom ( for a lot of users )
# мы можем и не посылать слаг, если создаем малтипл чат



    #     try:
            
    #     except Exception as ex:
    #                 print(f'Error in def message_create():\n\n{ex}')
    #                 return JsonResponse({'data': "0"})

    #     return JsonResponse({'data': "1"})#JsonResponse({'created': True})#HttpResponseRedirect(chat_to_write.get_absolute_url) # открываем не юрл сообщения а юрл чата

    # context = {
	# 	"c_form": c_form,
    # }
    # return JsonResponse({'data': render(request, 'create_msg_form.html', context)})



@login_required
def chat_create(request): #, auto):
# TODO сначала для 1 создадим, далее посмотрим
    if request.method == 'POST':

        data = request.POST.copy()
        c_form = None; people_in_chat = None # exclude me
        chat_name = None; c_instance=None; cu=None

        # if slug in dict of POST data -> initial creation of chat
        if 'slug' in data: # for 1 profile chat (initial) 
            # chat_name = "user1_to_user2"
            slug = data.get('slug')
            # HERE chat_name changing 1
            # слаги разные для каждого юзера, и если есть chat_name для связи 1-1, то он уникален
            chat_name = f'{slug}'#f'{request.user.profile.slug}_to_{slug}'
            people_in_chat = [Profile.objects.get(slug=slug)] # request.user.profile, 

            own_chats = request.user.profile.own_chats.all()
            print('\n\n\n')
            print(own_chats)
            try:
                if own_chats.filter(chat_name=chat_name).exists():
                    return HttpResponseRedirect(own_chats.get(chat_name=chat_name).get_absolute_url)
            except Chat.DoesNotExist:
                print('There is no own_chats at all')
                


            # HERE c_form changing 1
            # c_form = ChatUnionForm(people_in_chat=people_in_chat, chat_name=chat_name) # 'people_in_chat': people_in_chat=people_in_chat

            cu = ChatUnion.objects.create()
            c_instance = Chat(chat_name=chat_name, chat_owner=request.user.profile, chat_union = cu)
            c_instance.save()
            # after that will came creation chats for other relative users
        else: # create custom_chat
            # HERE c_form changing 2
            c_form = ChatUnionForm(request.POST or None)

            if c_form.is_valid():
                people_in_chat = c_form.cleaned_data['people_in_chat'] # 
                print(f'\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nshould be list:\n\n\n {type(people_in_chat)}') 
                if len(people_in_chat) > 0:
                    # people_in_chat = list(people_in_chat) # при том случае если был 1 чел в пипл и чат
                    # HERE chat_name changing 2
                    chat_name = c_form.cleaned_data['chat_name']
                    
                    print('step1')
                    cu = ChatUnion.objects.create()
                    
                    c_instance = c_form.save(commit=False)
                    c_instance.chat_union = cu # and for each other relative chat add that chat union
                    c_instance.chat_owner = request.user.profile # self
                    c_instance.save()
                    print('step2')
        

                else: # error
                    print('you should add users to chat to craete chat')
                    context = {
                    	"c_form": c_form,
                    	"error_c_form": "Chat Without Users Creation", # check it in template to show up msg that there no users choiced ( like not valid but for multipleform ) 
                    	# "base_template": "none.html",
                    }
                    # ajaxy
                    return JsonResponse({'data': str(render(request, 'create_chat_form.html', context))})
            else: # not filled form
                context = {
                    "c_form": c_form,
                    "error_c_form": "Not filled chat form",
                    # "base_template": "none.html",
                }
                # ajaxy
                return JsonResponse({'data': str(render(request, 'create_chat_form.html', context))})

        
        # все равно оба варика лист ( либо с 1 елема либо с кучи)

        cu.save()
        cu.refresh_from_db()
        print('step3')
        cu.create_chats_for_relative_users(request.user.profile, people_in_chat, chat_name)
        cu.save()
        print('step4')
        # [c_instance.people_in_chat.add(profile) for profile in people_in_chat]
        # c_instance.save()


        if 'slug' not in data:
            # ajaxy
            redirect(c_instance.get_absolute_url)
            # return JsonResponse({'created': True})
            return JsonResponse({'data': "1"})
        print('step5')
        # not ajaxy
        return HttpResponseRedirect(c_instance.get_absolute_url)
        # context = {
        # 	"m_form": m_form,
        # 	"c_form": c_form,
        # 	"theme": "Chat Create",
        # 	"base_template": "base.html",
        # }
    else:
        return HttpResponseBadRequest


@login_required
def chat_delete(request, slug=None): #DDDDDD
	# permission on only owner and admin can 
	if request.method == 'DELETE': # shold be only delete method for message deletion
		instance = get_object_or_404(Chat, slug=slug)
		instance.delete_chat()
		return redirect("chats:chat_list")
	return HttpResponseServerError()







# on profile page ( or in msgs bar )

# mini frame to write message (POST by ajax from chat list when we go to dhat details )
@login_required
def message_create(request, slug): #CCCCCC slug of chat in witch in will be created at first
    # permission on only auth-cated can
    print('\nWhile sending we see such data like:\n\n')
    print(request.POST)
    print(request.FILES)
    print('\nThats all\n')
    # print(request.get_full_path())
    
    m_form = MessageForm(request.POST or None, request.FILES or None)
    # print(m_form)
    # print('CheckStart\n')
    # print(m_form.cleaned_data['image'])
    # print(m_form.cleaned_data['content'])
    # print('CheckEnd\n')
    if m_form.is_valid(): # if content exists ( that is the one main validation )
        try:
            chat_to_write = Chat.objects.get(slug=slug)
            
            # c_instance = c_form.save(commit=False)
            # c_instance.save()

            message_model = m_form.save(commit=False) # content saved and image saved ( TOP )))))
            message_model.chat = chat_to_write
            message_model.sender = chat_to_write.chat_owner
            message_model.readed = True
            message_model.save()

            # populate msg to others in chat
            chat_to_write.chat_union.copy_chat_msgs(chat_to_write, message_model)
        except Exception as ex:
            print(f'Error in def message_create():\n\n{ex}')
            return JsonResponse({'data': "0"})
        # related_chats = chat_to_write.chat_union.get_related_chats(chat_to_write)

        # for chat in related_chats:
        #     chat.copy_msg(message_model)

        # m_inst.thread = c_instance

        # m_inst.sender = request.user.profile

        # m_inst.save()

        # m_inst.refresh_from_db()
        # [m_inst.receivers.add(r) for r in form.cleaned_data['receivers']]
        # # instance.receivers.save()
        # m_inst.save()

        return JsonResponse({'data': "1"})#JsonResponse({'created': True})#HttpResponseRedirect(chat_to_write.get_absolute_url) # открываем не юрл сообщения а юрл чата

    context = {
        "m_form": m_form,
    }
    # data = str((render(request, 'create_msg_form.html', context)).__dict__.get('_container')[0])
    data = ((render(request, 'create_msg_form.html', context)).__dict__.get('_container')[0]).decode("utf-8").replace("\r\n", "\n")
    pattern_to_add = f'="{request.get_full_path()}"'
    before_pattern_to_add = 'data-to-url'
    start_add_index = data.find(before_pattern_to_add) + len(before_pattern_to_add)
    data = f'{data[:start_add_index]}{pattern_to_add}{data[start_add_index:]}'
    # pattern_to_add = '<ul id="wmd-button-row-id_bio" class="wmd-button-row"><li class="wmd-button" id="wmd-bold-button-id_bio" title="Strong <strong> Ctrl+B" style="left: 0px;"><span style="background-position: 0px 0px;"></span></li><li class="wmd-button" id="wmd-italic-button-id_bio" title="Emphasis <em> Ctrl+I" style="left: 25px;"><span style="background-position: -20px 0px;"></span></li><li class="wmd-spacer wmd-spacer1" id="wmd-spacer1-id_bio"></li><li class="wmd-button" id="wmd-link-button-id_bio" title="Hyperlink <a> Ctrl+L" style="left: 75px;"><span style="background-position: -40px 0px;"></span></li><li class="wmd-button" id="wmd-quote-button-id_bio" title="Blockquote <blockquote> Ctrl+Q" style="left: 100px;"><span style="background-position: -60px 0px;"></span></li><li class="wmd-button" id="wmd-code-button-id_bio" title="Code Sample <pre><code> Ctrl+K" style="left: 125px;"><span style="background-position: -80px 0px;"></span></li><li class="wmd-button" id="wmd-image-button-id_bio" title="Image <img> Ctrl+G" style="left: 150px;"><span style="background-position: -100px 0px;"></span></li><li class="wmd-spacer wmd-spacer2" id="wmd-spacer2-id_bio"></li><li class="wmd-button" id="wmd-olist-button-id_bio" title="Numbered List <ol> Ctrl+O" style="left: 200px;"><span style="background-position: -120px 0px;"></span></li><li class="wmd-button" id="wmd-ulist-button-id_bio" title="Bulleted List <ul> Ctrl+U" style="left: 225px;"><span style="background-position: -140px 0px;"></span></li><li class="wmd-button" id="wmd-heading-button-id_bio" title="Heading <h1>/<h2> Ctrl+H" style="left: 250px;"><span style="background-position: -160px 0px;"></span></li><li class="wmd-button" id="wmd-hr-button-id_bio" title="Horizontal Rule <hr> Ctrl+R" style="left: 275px;"><span style="background-position: -180px 0px;"></span></li><li class="wmd-spacer wmd-spacer3" id="wmd-spacer3-id_bio"></li><li class="wmd-button" id="wmd-undo-button-id_bio" title="Undo - Ctrl+Z" style="left: 325px;"><span style="background-position: -200px -20px;"></span></li><li class="wmd-button" id="wmd-redo-button-id_bio" title="Redo - Ctrl+Y" style="left: 350px;"><span style="background-position: -220px -20px;"></span></li></ul>'
    # before_pattern_to_add = 'class="wmd-button-bar">'
    # start_add_index = data.find(before_pattern_to_add) + len(before_pattern_to_add)
    # data = f'{data[:start_add_index]}{pattern_to_add}{data[start_add_index:]}'
    # print('\ndata\n\n')
    # print(data)
    # print('\ndata\n\n\n')
    # [print(it) for it in data.__dict__]
    # print('\ndata\n\n\n')
    return JsonResponse({'data': data}) #JsonResponse({'created': False})#render(request, "create_msg_form.html", context) # return just generated  (form of corse)

        
        



# @login_required
# def message_detail(request, slug=None):
# 	instance = get_object_or_404(Message, slug=slug)
# 	context = {
# 		"topic": instance.topic,
# 		"instance": instance,
# 	}
# 	return render(request, "message_detail.html", context)


# @login_required
# def message_update(request, slug=None): #UUUUUU
# 	# permission on only owner and admin can update
# 	m_inst = get_object_or_404(Message, slug=slug)
# 	m_form = messageForm(request.POST or None, request.FILES or None, instance=m_inst)

# 	# mt_inst = get_object_or_404(message, id=id)
# 	# mt_form = messageThreadForm(request.POST or None, request.FILES or None, instance=mt_inst)

# 	if m_form.is_valid():

# 		# mt_inst = mt_form.save(commit=False)
# 		# mt_inst.save()

# 		m_inst = m_form.save(commit=False)

# 		m_inst.thread = mt_inst

# 		m_inst.save()



# 		return HttpResponseRedirect(m_inst.get_absolute_url)
# 	context = {
# 		"m_form": m_form,
# 		"mt_form": mt_form,
# 		"theme": "message Update",
# 		"base_template": "base.html",
# 	}
# 	return render(request, "ultimate_form.html", context)

# @login_required
# def message_delete(request, id=None): #DDDDDD
# 	# permission on only owner and admin can 
# 	if request.method == 'DELETE': # shold be only delete method for message deletion
# 		instance = get_object_or_404(Message, id=id)
# 		instance.delete()
# 		return redirect("chats:list")
# 	return HttpResponseServerError()

