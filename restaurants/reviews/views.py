from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ReviewForm
import datetime
from .models import Review, Restaurant


# get a list of the latest 9 reviews and renders it using reviews/list.html
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


# get a review given its ID and renders it using review_detail.html
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


# get all the restaurant sorted by name and passes it to restaurant_list.html to be rendered.
def restaurant_list(request):
    restaurant = Restaurant.objects.order_by('-name')
    context = {'restaurant_list':restaurant_list}
    return render(request, 'reviews/restaurant_list.html', context)


# gets a restaurant from the DB given its ID and renders it using restaurant_detail.html
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'reviews/restaurant_detail.html', {'restaurant': restaurant})



def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.restaurant = restaurant
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:restaurant_detail', args=(restaurant.id,)))

    return render(request, 'reviews/restaurant_detail.html', {'restaurant': restaurant, 'form': form})
