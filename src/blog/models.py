# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     models.py
   Description :
   Author :       JHao
   date：          2016/11/18
-------------------------------------------------
   Change Activity:
                   2016/11/18:
-------------------------------------------------
"""
import datetime

from PIL import Image
from django.db import models
from django.conf import settings
import ckeditor.fields


# Create your models here.
from django.utils.html import format_html

from blog.storage import PathAndRename


class Tag(models.Model):
    tag_name = models.CharField('标签名称', max_length=30)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=200)  # 博客标题
    category = models.ForeignKey('Category', verbose_name='文章类型', on_delete=models.CASCADE)
    date_time = models.DateField(auto_now_add=True)  # 博客日期
    # content = models.TextField(blank=True, null=True)  # 文章正文
    content = ckeditor.fields.RichTextField()  # 使用富文本编辑器
    digest = models.TextField(blank=True, null=True)  # 文章摘要
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    view = models.BigIntegerField(default=0)  # 阅读数
    comment = models.BigIntegerField(default=0)  # 评论数
    picture = models.CharField(max_length=200)  # 标题图片存放文件夹
    picture_img = models.ImageField(upload_to='article/%Y%m%d/', blank=True)  # 图片存放的完整路径
    tag = models.ManyToManyField(Tag)  # 标签

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 在保存对象之前更新 image_url 字段
        today = datetime.date.today().strftime('%Y%m%d')
        self.picture = "/media/article/{}/".format(today) + str(self.picture_img)
        super(Article, self).save(*args, **kwargs)

        img = Image.open(self.picture_img.path)
        if img.height > 200 or img.width > 300:
            output_size = (200, 300)
            img.thumbnail(output_size)
            img.save(self.picture_img.path)

    def sourceUrl(self):
        source_url = settings.HOST + '/blog/detail/{id}'.format(id=self.pk)
        return source_url  # 给网易云跟帖使用

    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])

    def commenced(self):
        """
        增加评论数
        :return:
        """
        self.comment += 1
        self.save(update_fields=['comment'])

    class Meta:  # 按时间降序
        ordering = ['-date_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField('文章类型', max_length=30)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    title = models.CharField("标题", max_length=100)
    source_id = models.CharField('文章id或source名称', max_length=25)
    create_time = models.DateTimeField('评论时间', auto_now=True)
    user_name = models.CharField('评论用户', max_length=25)
    url = models.CharField('链接', max_length=100)
    comment = models.CharField('评论内容', max_length=500)


class PhotoGroup(models.Model):
    name = models.CharField(u'标题', max_length=150, unique=True)
    cover = models.ImageField(upload_to=PathAndRename("photocover"), verbose_name=u'封面')
    desc = models.TextField(u'描述', )
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    active = models.BooleanField(u'开启', default=True)

    class Meta:
        verbose_name = u'相册'
        verbose_name_plural = u'相册'

    def __str__(self):
        return self.name


class Photo(models.Model):
    photo = models.ImageField(upload_to=PathAndRename("photo"), verbose_name=u'照片')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')
    group = models.ForeignKey('PhotoGroup', on_delete=models.CASCADE, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        verbose_name = u'照片'
        verbose_name_plural = u'照片'

    def view_img(self):
        return format_html("<img src='/media/%s' height='200'/>" % self.photo)

    view_img.short_description = '预览'
    view_img.allow_tags = True

    # def save(self, *args, **kwargs):
    #     # 在保存对象之前更新 image_url 字段
    #     print(self.photo.path)
    #     img = Image.open(self.photo.path)
    #     if img.height > 200 or img.width > 300:
    #         output_size = (200, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.photo.path)