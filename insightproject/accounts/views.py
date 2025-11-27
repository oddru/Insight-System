from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from .models import Account, Transaction

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create account with starting balance
            Account.objects.create(user=user, balance=1000.00)
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard instead of home
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard instead of home
        else:
            error_message = "No account detected. Please check your email and password or register a new account."
    return render(request, 'users/home.html', {'error_message': error_message, 'show_modal': True, 'form': UserCreationForm()})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')

def user_home(request):
    form = UserCreationForm()
    return render(request, "users/home.html", {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    # Get or create account
    account, created = Account.objects.get_or_create(user=request.user)
    
    # Get recent transactions (both sent and received) then dedupe paired records
    qs = (Transaction.objects.filter(receiver=request.user) | Transaction.objects.filter(sender=request.user)).order_by('-timestamp')[:50]
    # Deduplicate logical transfers: if both a 'transfer' and a 'received' record exist
    # for the same sender/receiver/amount/timestamp we only keep one.
    seen = set()
    transactions = []
    for t in qs:
        # build a simple key to detect duplicates
        key = (t.sender_id or 0, t.receiver_id or 0, str(t.amount), t.timestamp.replace(microsecond=0))
        if key in seen:
            continue
        # also check reversed pair (in case ordering differs)
        rev_key = (t.receiver_id or 0, t.sender_id or 0, str(t.amount), t.timestamp.replace(microsecond=0))
        if rev_key in seen:
            continue
        seen.add(key)
        transactions.append(t)

    context = {
        'account': account,
        'transactions': transactions[:10],
    }
    return render(request, "users/dashboard.html", context)

def deposit_tokens(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount > 0:
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                
                # Create transaction record
                Transaction.objects.create(
                    receiver=request.user,
                    amount=amount,
                    transaction_type='deposit',
                    description=f'Deposit of {amount} tokens'
                )
                
                return redirect('dashboard')
        except (ValueError, Account.DoesNotExist):
            pass
    
    return redirect('dashboard')

def transfer_tokens(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        amount = request.POST.get('amount')
        error_message = None
        
        try:
            amount = Decimal(amount)
            sender_account = Account.objects.get(user=request.user)
            receiver_user = User.objects.get(username=receiver_username)
            receiver_account = Account.objects.get(user=receiver_user)
            
            # Validation
            if request.user == receiver_user:
                error_message = "Cannot transfer to yourself"
            elif amount <= 0:
                error_message = "Amount must be greater than 0"
            elif sender_account.balance < amount:
                error_message = "Insufficient balance"
            else:
                # Use database transaction to ensure atomicity
                with transaction.atomic():
                    sender_account.balance -= amount
                    sender_account.save()
                    
                    receiver_account.balance += amount
                    receiver_account.save()
                    
                    # Create transaction records
                    Transaction.objects.create(
                        sender=request.user,
                        receiver=receiver_user,
                        amount=amount,
                        transaction_type='transfer',
                        description=f'Transfer to {receiver_user.username}'
                    )
                    # Single transaction record is created. Direction (sent/received)
                    # will be derived relative to the requesting user when returning data.
                
                return redirect('dashboard')
        except (ValueError, User.DoesNotExist, Account.DoesNotExist):
            error_message = "Invalid transfer details"
        
        context = {'error_message': error_message}
        return redirect('dashboard')
    
    return redirect('dashboard')


@require_http_methods(["GET"])
def get_transactions(request):
    """API endpoint to get user's transactions in JSON format"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    qs = (Transaction.objects.filter(receiver=request.user) | Transaction.objects.filter(sender=request.user)).order_by('-timestamp')[:50]
    seen = set()
    tx_list = []
    for t in qs:
        key = (t.sender_id or 0, t.receiver_id or 0, str(t.amount), t.timestamp.replace(microsecond=0))
        rev_key = (t.receiver_id or 0, t.sender_id or 0, str(t.amount), t.timestamp.replace(microsecond=0))
        if key in seen or rev_key in seen:
            continue
        seen.add(key)
        tx_list.append(t)

    data = {
        'transactions': [
            {
                'id': t.id,
                'amount': float(t.amount),
                'type': t.transaction_type,
                'sender': t.sender.username if t.sender else 'System',
                'receiver': t.receiver.username,
                'timestamp': t.timestamp.isoformat(),
                'description': t.description,
                # direction is relative to the requesting user: 'sent' | 'received' | 'deposit'
                'direction': (
                    'deposit' if t.transaction_type == 'deposit' and t.receiver == request.user else
                    'received' if t.receiver == request.user else
                    'sent'
                )
                ,
                # Pre-compute display strings so client doesn't rely on DB description
                'display_label': (
                    ('Demo Deposit') if t.transaction_type == 'deposit' and t.receiver == request.user else
                    (f'From {t.sender.username}' if t.sender and t.receiver == request.user else f'To {t.receiver.username}')
                ),
                'display_description': (
                    (t.description if t.transaction_type == 'deposit' else
                     (f'Received from {t.sender.username}' if t.receiver == request.user else f'Transfer to {t.receiver.username}'))
                ),
            }
            for t in tx_list[:10]
        ]
    }
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_balance(request):
    """API endpoint to get current user balance"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        account = Account.objects.get(user=request.user)
        return JsonResponse({'balance': float(account.balance)})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)