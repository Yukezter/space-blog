from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView, ListView

from wagtail.search.models import Query

from blog.views import BlogPage

class Home(TemplateView):
    template_name = 'pages/home.html'

def category(request, category):
    posts = BlogPage.objects.live().order_by('-date').filter(category=category)[:5]
    posts_count = posts.count

    category = category.title()

    context = {
        'posts': posts,
        'posts_count': posts_count,
        'category': category,
    }

    return render(request, 'pages/category.html', context)

# class Category(TemplateView):
#     template_name = 'pages/category.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         category = kwargs['category']
#         posts = BlogPage.objects.live().order_by('-date').filter(category=category)[:5]
#         posts_count = posts.count
#
#         print(posts)
#
#         category = category.title()
#
#         context['posts'] = posts
#         context['posts_count'] = posts_count
#         context['category'] = category
#
#         return context

def search(request):

    if request.method == 'GET':
        search_query = request.GET.get('query', None)
        page = request.GET.get('page', 1)

        # Search
        if search_query:
            search_results = BlogPage.objects.live().order_by('-date').search(search_query, fields=['title', 'subtitle'])
            query = Query.get(search_query)
            posts_count = search_results.count

            # Record hit
            query.add_hit()
        else:
            search_results = BlogPage.objects.none()
            posts_count = 0

        # Pagination
        paginator = Paginator(search_results, 5)
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

        context = {
            'search_query': search_query,
            'posts_count': posts_count,
            'posts': search_results,
        }

        return render(request, 'pages/search.html', context)