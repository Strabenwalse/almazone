from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import AdForm, ProductForm
from .models import Ad, Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .forms import UserEditForm
from django.contrib.auth import login
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # или на 'edit_profile', как тебе удобнее
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'accounts/user_edit.html', {'form': form})
def home(request):
    return render(request, 'sitte/home.html')
# Главная страница
def some_view(request):
    return redirect(reverse('ad_list'))
def save_theme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        user.theme = data.get('theme', 'light')
        user.save()
        return JsonResponse({'status': 'success'})
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
# Список объявлений с фильтрацией, сортировкой и AJAX поддержкой
# Список объявлений с фильтрацией
def ad_list(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    sort_by = request.GET.get('sort_by', 'date')

    ads = Ad.objects.all()

    # Преобразуем фильтры в числа, если они присутствуют
    if price_min:
        price_min = float(price_min)
        ads = ads.filter(price__gte=price_min)
    if price_max:
        price_max = float(price_max)
        ads = ads.filter(price__lte=price_max)

    if search_query:
        ads = ads.filter(title__icontains=search_query)
    if category_id:
        ads = ads.filter(category_id=category_id)

    if sort_by == 'price_asc':
        ads = ads.order_by('price')
    elif sort_by == 'price_desc':
        ads = ads.order_by('-price')
    else:
        ads = ads.order_by('-created_at')

    paginator = Paginator(ads, 9)
    page = request.GET.get('page', 1)
    ads_page = paginator.get_page(page)

    context = {
        'ads': ads_page,
        'categories': Category.objects.all(),
        'selected_category': category_id,
        'price_min': price_min,
        'price_max': price_max,
        'sort_by': sort_by
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/ad_items.html', context)

    return render(request, 'ads/ad_list.html', context)


# Детали объявления
@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    # Проверка, что пользователь является автором объявления
    if ad.author != request.user:
        return redirect('ad_list')

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/ad_create.html', {'form': form, 'ad': ad})
# Удаление объявления
@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.author != request.user:
        return redirect('ad_list')

    ad.delete()
    return redirect('ad_list')

# Создание объявления
@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            print(f"Загружено изображение: {ad.image.url if ad.image else 'Нет изображения'}")
            return redirect('ad_list')
    else:
        form = AdForm()

    return render(request, 'ads/ad_create.html', {'form': form})

# Страница с последними объявлениями
def index(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'base.html', {'ads': ads})

# Создание продукта
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'sitte/create_product.html', {'form': form})

# Объявления текущего пользователя
@login_required
def my_ads(request):
    ads = Ad.objects.filter(author=request.user)
    return render(request, 'my_ads.html', {'ads': ads})

# Детали объявления
def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

def user_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # перенаправление обратно на страницу профиля
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/user_edit.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на домашнюю страницу
    else:
        form = UserEditForm()

    return render(request, 'accounts/register.html', {'form': form})