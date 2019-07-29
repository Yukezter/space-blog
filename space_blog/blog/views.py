from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from wagtail.search.models import Query

from .models import BlogPage


# This function is called via ajax when the 'more posts' button is clicked
# The data passed by ajax is used to filter what queryset we need
def lazy_load_posts(request):

    if request.is_ajax():

        # Get ajax data
        page = request.POST.get('page')
        # Only one of these two will have a value
        search_query = request.POST.get('query')
        category = request.POST.get('category')

        # Check which one is not None and get queryset
        if search_query:
            search_results = BlogPage.objects.live().order_by('-date').search(search_query,
                                                                               fields=['title', 'subtitle'])
        elif category:
            search_results = BlogPage.objects.live().order_by('-date').filter(category=category)
        else:
            # If there is neither a search query or category,
            # just get all the live BlogPage objects
            search_results = BlogPage.objects.live().order_by('-date')

        # Pagination
        paginator = Paginator(search_results, 5)
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(2)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

        # This is what is appended to the posts list container
        posts_html = loader.render_to_string('blog/includes/posts.html', {'posts': search_results})

        # Package output data and return it as a JSON object
        output_data = {
            'posts_html': posts_html,
            'has_next': search_results.has_next()
        }
        return JsonResponse(output_data)
    else:
        return render(request, '404.html')