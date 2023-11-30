from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo
from django.contrib.auth.models import User
from base64 import b64decode
from django.contrib.auth import authenticate

class TodosView(View):
    def get(self, request: HttpRequest) -> HttpRequest:
        header =request.headers
        auth = header['Authorization']['6:']
        username, password = b64decode(auth).decode().split(":")

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized"}, status=401)
        result=[]
        for todo in user.todos.all():
            result.append(model_to_dict(todo))        
        return JsonResponse(result, safe=False)
class TodosView(View):
    def get(self, request: HttpRequest, user_id: int) -> HttpRequest:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user not found.'})
        todos = Todo.objects.filter(user=user)

        result = []
        for todo in todos:
            result.append(model_to_dict(todo))
        
        return JsonResponse(result, safe=False)
