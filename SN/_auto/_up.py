from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
# import posts.models as posts_models #Post
# import likes.models as likes_models #Like
import random

# import pickle

def get_password_or_name(key='name'):
    symb_to_choice = [[33, 35, 36, 37, 38, 42, 64, 94], 
        list(range(48,58)), list(range(65, 91)), list(range(97, 123))] # # ==== !@#$%^&*  ///////// 33,126 
    nums_to_choice = list(range(48,58)) # 0 - 9
    upper_case_letters = list(range(65, 91))
    lower__case_letters = list(range(97, 123))
    all_symbols = sum(symb_to_choice, []) if key == 'password' else sum(symb_to_choice[1:], [])
    gener_len = random.randint(8, 16) #  8-16 symbols in password
    gener = []
    for i in range(gener_len):
        gener.append(random.choice(all_symbols)) # ascii symbols
    gener = [chr(i) for i in gener]
    return ''.join(gener)


def dump_users(filename, data):
    with open(filename, 'w') as f: # a
        f.write(str(data))


def populate_users(num):
    emails = 'billyrusslee@gmail.com'
    filename =  r'_auto/users.txt'
    user_data = [{'username': get_password_or_name(), 'password': get_password_or_name(key='password'), 'id': u, 'email': emails} for u in range(2, num + 2)] # id = 1 for admin
    dump_users(filename, user_data)
    [User.objects.create_user(username = u['username'], password = u['password'], email = u['email']) for u in user_data]
    del user_data

# def get_post_user(num=None, id=None):
#     return User.objects.get(id=random.choice(range(2, num + 2))) if id is None else User.objects.get(id=id)

# def populate_posts(posts, users): # rand numof posts for each user    ###user=User.objects.get(username
#     for post in range(posts):
#         posts_models.Post.objects.create(title=f'title {get_password_or_name()}', content=f'content {get_password_or_name()}', owner=get_post_user(num=users)) # no image

# def populate_likes(likes, posts, users):  # rand numof likes for each post
#     # 2 likes at least or for latest posts 0 likes in likes if they are out of range
#     min_likes_per_post = likes / posts 
#     for post_id in range(1, posts + 1):
#         userset = set(range(2, users + 2))
#         # num of likes on post from min_likes_per_post to num of users or 0
#         for like in range(random.randint(min_likes_per_post, len(userset))): 
#             if likes == 0:
#                 del userset
#                 return None
#             post_like = likes_models.Like.objects.create(user=get_post_user(id=userset.pop()), post=posts_models.Post.objects.get(id=post_id))
#             # get_or_create return tuple (obj, True) while creating instance, while create return obj
#             # даже не проверяем на то что один и тот же юзер мог дважды пролукасить так как тут попом вытесняются повторяющиеся юзеры
#             # no vse zhe zachemto zapisali eto
#             post_like.value = 1
#             post_like.save()
#             likes -= 1
#         del userset


def main(users):
    print(f'populate {users} users')
    populate_users(users)
#     print(f'populate {posts} posts')
#     populate_posts(posts, users)
#     print(f'populate {likes} likes')
#     populate_likes(likes, posts, users)
#     print('popoulation was ended')

num_of_users = 20
# num_of_posts = 40
# num_of_likes = 80
main(num_of_users)
# main(num_of_users, num_of_posts, num_of_likes)