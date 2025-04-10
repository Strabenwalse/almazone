from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad
from .forms import AdForm
from django.contrib.auth.decorators import login_required


def ad_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ad_list.html', {'ads': ads})


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_create.html', {'form': form})


def index(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/base.html', {'ads': ads})

