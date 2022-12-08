from mysite.user_accounts.forms import CreateAccountForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, '../user_accounts/templates/login.html')

def contact(request):
    form = CreateAccountForm()
    return render(request, '../user_accounts/templates/profile.html', {'form': form})
