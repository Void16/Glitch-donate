from django.shortcuts import render, redirect
from .forms import DonationForm
from .models import Donation
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from django.db.models import Sum, Max
import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

@login_required
def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            return redirect('my_donations')
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form})

@login_required
def my_donations(request):
    donations = Donation.objects.filter(user=request.user)
    return render(request, 'my_donations.html', {'donations': donations})

#to remove
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_donations = Donation.objects.count()
    total_amount = Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    highest_donation = Donation.objects.aggregate(Max('amount'))['amount__max'] or 0

    # Get donation data grouped by day
    daily_data = (Donation.objects
                  .annotate(date=TruncDate('timestamp'))
                  .values('date')
                  .annotate(total=Sum('amount'))
                  .order_by('date'))

    labels = [entry['date'].strftime('%Y-%m-%d') for entry in daily_data]
    data = [float(entry['total']) for entry in daily_data]

    context = {
        'total_users': total_users,
        'total_donations': total_donations,
        'total_amount': total_amount,
        'highest_donation': highest_donation,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    return render(request, 'donations/admin_dashboard.html', context)
