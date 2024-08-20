# -*- coding: utf-8 -*-
# Create your views here.

import json
from django.http import JsonResponse
from django.views.generic import ListView
from django_blog.util import PageInfo
from blog.models import Article, Comment
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from blog.models import PhotoGroup, Photo


def get_page(request):
    page_number = request.GET.get("page")
    return 1 if not page_number or not page_number.isdigit() else int(page_number)


def index(request):
    _blog_list = Article.objects.all().order_by('-date_time')[0:5]
    _blog_hot = Article.objects.all().order_by('-view')[0:6]
    return render(request, 'blog/index.html', {"blog_list": _blog_list, "blog_hot": _blog_hot})


def blog_list(request):
    """
    列表
    :param request:
    :return:
    """
    page_number = get_page(request)
    blog_count = Article.objects.count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.all()[page_info.index_start: page_info.index_end]
    return render(request, 'blog/list.html', {"blog_list": _blog_list, "page_info": page_info})


def category(request, name):
    """
    分类
    :param request:
    :param name:
    :return:
    """
    page_number = get_page(request)
    blog_count = Article.objects.filter(category__name=name).count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.filter(category__name=name)[page_info.index_start: page_info.index_end]
    return render(request, 'blog/category.html', {"blog_list": _blog_list, "page_info": page_info,
                                                  "category": name})


def tag(request, name):
    """
    标签
    :param request:
    :param name
    :return:
    """
    page_number = get_page(request)
    blog_count = Article.objects.filter(tag__tag_name=name).count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.filter(tag__tag_name=name)[page_info.index_start: page_info.index_end]
    return render(request, 'blog/tag.html', {"blog_list": _blog_list,
                                             "tag": name,
                                             "page_info": page_info})


def archive(request):
    """
    文章归档
    :param request:
    :return:
    """
    _blog_list = Article.objects.values("id", "title", "date_time").order_by('-date_time')
    archive_dict = {}
    for blog in _blog_list:
        pub_month = blog.get("date_time").strftime('%Y{y}%m{m}').format(y='年', m='月')
        if pub_month in archive_dict:
            archive_dict[pub_month].append(blog)
        else:
            archive_dict[pub_month] = [blog]
    data = sorted([{"date": _[0], "blogs": _[1]} for _ in archive_dict.items()], key=lambda item: item["date"],
                  reverse=True)
    return render(request, 'blog/archive.html', {"data": data})


def message(request):
    return render(request, 'blog/message_board.html', {"source_id": "message"})


@csrf_exempt
def get_comment(request):
    """
    接收畅言的评论回推， post方式回推
    :param request:
    :return:
    """
    arg = request.POST
    data = arg.get('data')
    data = json.loads(data)
    title = data.get('title')
    url = data.get('url')
    source_id = data.get('sourceid')
    if source_id not in ['message']:
        article = Article.objects.get(pk=source_id)
        article.commenced()
    comments = data.get('comments')[0]
    content = comments.get('content')
    user = comments.get('user').get('nickname')
    Comment(title=title, source_id=source_id, user_name=user, url=url, comment=content).save()
    return JsonResponse({"status": "ok"})


def detail(request, pk):
    """
    博文详情
    :param request:
    :param pk:
    :return:
    """
    blog = get_object_or_404(Article, pk=pk)
    blog.viewed()
    return render(request, 'blog/detail.html', {"blog": blog})


def search(request):
    """
    搜索
    :param request:
    :return:
    """
    key = request.GET['key']
    page_number = get_page(request)
    blog_count = Article.objects.filter(title__icontains=key).count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.filter(title__icontains=key)[page_info.index_start: page_info.index_end]
    return render(request, 'blog/search.html', {"blog_list": _blog_list, "pages": page_info, "key": key})


def page_not_found_error(request, exception):
    return render(request, "404.html", status=404)


def page_error(request):
    return render(request, "404.html", status=500)


class PhotoGroupView(ListView):
    """
    首页
    """
    template_name = 'photogroup.html'
    context_object_name = "photogroups"
    queryset = PhotoGroup.objects.filter(active=True)
    paginate_by = 2
    ordering = '-create_time'

    def get_context_data(self, **kwargs):
        context = super(PhotoGroupView, self).get_context_data(**kwargs)
        return context


class PhotoView(ListView):
    """
    首页
    """
    template_name = 'photo.html'
    context_object_name = "photos"
    queryset = Photo.objects.all()

    def get_queryset(self):
        group = self.kwargs.get('group')
        context = super(PhotoView, self).get_queryset().filter(group__name=group)
        return context

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)

        group = self.kwargs.get('group')
        group_id = PhotoGroup.objects.get(name=group).id

        prev_post = None
        next_post = None

        try:
            prev_post = PhotoGroup.objects.get(active=True, pk=(group_id - 1))
        except Exception as e:
            print(e)

        try:
            next_post = PhotoGroup.objects.get(active=True, pk=(group_id + 1))
        except Exception as e:
            print(e)

        context['prev_post'] = prev_post
        context['next_post'] = next_post
        return context