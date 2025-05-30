from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import AdForm, ProductForm
from .models import Category
from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm
from django.contrib.auth import login
from .models import Ad
import json
from django.http import HttpResponseForbidden
from .forms import AdImageForm

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
def ad_list(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    sort_by = request.GET.get('sort_by', 'date')

    ads = Ad.objects.all()

    # Фильтрация по минимальной цене
    if price_min:
        try:
            price_min = float(price_min)
            ads = ads.filter(price__gte=price_min)
        except ValueError:
            pass  # Если некорректное значение, просто пропускаем фильтрацию

    # Фильтрация по максимальной цене
    if price_max:
        try:
            price_max = float(price_max)
            ads = ads.filter(price__lte=price_max)
        except ValueError:
            pass  # Если некорректное значение, просто пропускаем фильтрацию

    # Поиск по запросу
    if search_query:
        ads = ads.filter(title__icontains=search_query)

    # Фильтрация по категории
    if category_id:
        try:
            category_id = int(category_id)
            ads = ads.filter(category_id=category_id)
        except ValueError:
            pass  # Если некорректное значение, просто пропускаем фильтрацию

    # Сортировка
    if sort_by == 'price_asc':
        ads = ads.order_by('price')
    elif sort_by == 'price_desc':
        ads = ads.order_by('-price')
    else:
        ads = ads.order_by('-created_at')

    # Пагинация
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

    # Для AJAX-запросов рендерим только список объявлений
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/ad_items.html', context)

    return render(request, 'ads/ad_list.html', context)

# Детали объявления
@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if request.user != ad.author:
        return HttpResponseForbidden("У вас нет прав на редактирование этого объявления.")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', pk=ad.pk)
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
            return redirect('ad_detail', pk=ad.pk)
        # Ветка else убираем, просто рендерим с текущей формой с ошибками
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

@login_required
def ad_image_view(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    form = AdImageForm(request.POST or None, request.FILES or None, instance=ad)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ad_detail', ad_id=ad.id)

    return render(request, 'ads/ad_image.html', {
        'form': form,
        'ad': ad,  # << ЭТО ОБЯЗАТЕЛЬНО
    })
