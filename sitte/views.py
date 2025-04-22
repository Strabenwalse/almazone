from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import AdForm, ProductForm

# Главная страница
def some_view(request):
    return redirect(reverse('ad_list'))
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from .models import Ad, Category

def ad_list(request):
    ads = Ad.objects.all()
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category:
        ads = ads.filter(category__id=category)
    if min_price:
        ads = ads.filter(price__gte=min_price)
    if max_price:
        ads = ads.filter(price__lte=max_price)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/ad_items.html', {'ads': ads})

    categories = Category.objects.all()
    return render(request, 'ads/ad_list.html', {'ads': ads, 'categories': categories})

def ad_list(request):
    # Обработка фильтров
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    sort_by = request.GET.get('sort_by', 'date')

    ads = Ad.objects.all()

    if search_query:
        ads = ads.filter(title__icontains=search_query)
    if category_id:
        ads = ads.filter(category_id=category_id)
    if price_min:
        ads = ads.filter(price__gte=price_min)
    if price_max:
        ads = ads.filter(price__lte=price_max)

    if sort_by == 'price_asc':
        ads = ads.order_by('price')
    elif sort_by == 'price_desc':
        ads = ads.order_by('-price')
    else:
        ads = ads.order_by('-created_at')

    # Пагинация
    page = request.GET.get('page', 1)
    paginator = Paginator(ads, 9)  # 9 объявлений на страницу
    ads_page = paginator.get_page(page)

    # Если запрос через AJAX, возвращаем только список
    if request.is_ajax():
        return render(request, 'partials/ad_items.html', {'ads': ads_page})

    return render(request, 'ads/ad_list.html', {
        'ads': ads_page,
        'categories': Category.objects.all(),
        'selected_category': category_id,
        'price_min': price_min,
        'price_max': price_max,
        'sort_by': sort_by
    })

    return render(request, 'ads/ad_list.html', context)


# Детали объявления
@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    # Проверяем, является ли текущий пользователь автором объявления
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

    # Проверяем, является ли текущий пользователь автором объявления
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

            # Отладка (можно убрать позже)
            print(f"Загружено изображение: {ad.image.url if ad.image else 'Нет изображения'}")
            return redirect('ad_list')
    else:
        form = AdForm()

    return render(request, 'ads/ad_create.html', {'form': form})

# Страница с последними объявлениями
def index(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'base.html', {'ads': ads})

# Создание продукта (если нужно)
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
