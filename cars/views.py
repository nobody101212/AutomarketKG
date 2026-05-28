from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Car, Brand, CarModel, CarImage, Favorite, Message
from .forms import CarForm


def home(request):
    featured_cars = Car.objects.filter(is_active=True, is_featured=True).prefetch_related('images')[:8]
    recent_cars = Car.objects.filter(is_active=True).prefetch_related('images')[:12]
    brands = Brand.objects.annotate(car_count=Count('car')).filter(car_count__gt=0).order_by('-car_count')[:12]
    total_cars = Car.objects.filter(is_active=True).count()
    return render(request, 'cars/home.html', {
        'featured_cars': featured_cars, 'recent_cars': recent_cars,
        'brands': brands, 'total_cars': total_cars,
    })


def car_list(request):
    cars = Car.objects.filter(is_active=True).select_related('brand', 'model', 'seller').prefetch_related('images')

    brand_id = request.GET.get('brand')
    model_id = request.GET.get('model')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    transmission = request.GET.get('transmission')
    fuel_type = request.GET.get('fuel_type')
    condition = request.GET.get('condition')
    city = request.GET.get('city')
    q = request.GET.get('q')

    if q:
        cars = cars.filter(Q(brand__name__icontains=q) | Q(model__name__icontains=q) | Q(description__icontains=q))
    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if model_id:
        cars = cars.filter(model_id=model_id)
    if year_from:
        cars = cars.filter(year__gte=year_from)
    if year_to:
        cars = cars.filter(year__lte=year_to)
    if price_from:
        cars = cars.filter(price__gte=price_from)
    if price_to:
        cars = cars.filter(price__lte=price_to)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if condition:
        cars = cars.filter(condition=condition)
    if city:
        cars = cars.filter(city__icontains=city)

    sort = request.GET.get('sort', '-created_at')
    sort_map = {'-created_at': '-created_at', 'price_asc': 'price', 'price_desc': '-price',
                'year_desc': '-year', 'year_asc': 'year'}
    cars = cars.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(cars, 20)
    cars_page = paginator.get_page(request.GET.get('page'))

    return render(request, 'cars/car_list.html', {
        'cars': cars_page,
        'brands': Brand.objects.all(),
        'total_count': paginator.count,
        'sort': sort,
        'current_filters': request.GET.dict(),
    })


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk, is_active=True)
    car.views_count += 1
    car.save(update_fields=['views_count'])

    similar = Car.objects.filter(is_active=True, brand=car.brand).exclude(pk=pk).prefetch_related('images')[:4]
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, car=car).exists()

    return render(request, 'cars/car_detail.html', {
        'car': car, 'similar_cars': similar, 'is_favorite': is_favorite,
    })


@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.save()
            for i, img in enumerate(request.FILES.getlist('images')):
                CarImage.objects.create(car=car, image=img, is_main=(i == 0))
            messages.success(request, 'Объявление создано!')
            return redirect('cars:car_detail', pk=car.pk)
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form, 'brands': Brand.objects.all(), 'action': 'create'})


@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            for img in request.FILES.getlist('images'):
                CarImage.objects.create(car=car, image=img)
            messages.success(request, 'Обновлено!')
            return redirect('cars:car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/car_form.html', {'form': form, 'car': car, 'brands': Brand.objects.all(), 'action': 'edit'})


@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk, seller=request.user)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Удалено!')
        return redirect('accounts:my_ads')
    return render(request, 'cars/car_confirm_delete.html', {'car': car})


@login_required
def car_toggle_active(request, pk):
    car = get_object_or_404(Car, pk=pk, seller=request.user)
    if request.method == 'POST':
        car.is_active = not car.is_active
        car.save()
        messages.success(request, f"Объявление {'активировано' if car.is_active else 'деактивировано'}!")
    return redirect('accounts:my_ads')


@login_required
def toggle_favorite(request, pk):
    car = get_object_or_404(Car, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, car=car)
    if not created:
        fav.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})


def get_models(request):
    models = CarModel.objects.filter(brand_id=request.GET.get('brand_id')).values('id', 'name')
    return JsonResponse({'models': list(models)})


def brand_list(request):
    brands = Brand.objects.annotate(car_count=Count('car')).order_by('name')
    return render(request, 'cars/brand_list.html', {'brands': brands})


@login_required
def chat(request, car_pk, user_pk):
    car = get_object_or_404(Car, pk=car_pk)
    other_user = get_object_or_404(User, pk=user_pk)

    messages_list = Message.objects.filter(car=car).filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    messages_list.filter(receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(sender=request.user, receiver=other_user, car=car, text=text)
            return redirect('cars:chat', car_pk=car_pk, user_pk=user_pk)

    return render(request, 'cars/chat.html', {
        'car': car, 'other_user': other_user, 'messages_list': messages_list,
    })


@login_required
def my_chats(request):
    chats = []
    seen = set()
    for msg in Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('car', 'sender', 'receiver').order_by('-created_at'):
        key = (msg.car_id, min(msg.sender_id, msg.receiver_id), max(msg.sender_id, msg.receiver_id))
        if key not in seen:
            seen.add(key)
            other = msg.receiver if msg.sender == request.user else msg.sender
            unread = Message.objects.filter(car=msg.car, sender=other, receiver=request.user, is_read=False).count()
            chats.append({'car': msg.car, 'other_user': other, 'last_message': msg, 'unread': unread})

    return render(request, 'cars/my_chats.html', {'chats': chats})