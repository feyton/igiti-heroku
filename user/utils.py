from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'This email is taken'
    return JsonResponse(data)
