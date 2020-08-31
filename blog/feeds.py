from blog.models import BlogPage
from django.contrib.syndication.views import Feed

class LatestBlogFeed(Feed):
    title = "Эко-новости в Омске"
    link = "/блог/"
    description = "Новости публикует проект EcoLab мастерская где каждый желающий может переработать свой пластик в новую практичную вещь."

    def items(self):
        return BlogPage.objects.order_by('-last_published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.specific.intro

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_full_url()