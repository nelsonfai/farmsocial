from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import UserQA
# Create your views here.


@login_required
def myagricAi(request):
    chat = UserQA.objects.filter(user=request.user)
    return render(request, 'ai/chatroom.html',{'chatbot':chat})

@login_required 
def aiChat_room(request,):
    question = request.POST['question']
    try:    
        answer = openai(question)
        #answer='this is the responsw'
        obj =UserQA(user=request.user,question=question,answer=answer)
        obj.save()
        return JsonResponse({'response': answer })
    except Exception as e:
        print(e)
        return JsonResponse({'response': 'No information available at this moment.Please try again later '})

def openai(question):
    import os
    import openai
    openai.api_key = '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'
    prompt=f'{question}\n'
    print(prompt)
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt = question,
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    )
    print(response)
    if response.choices[0].text:
      answer = response.choices[0].text
    
    return answer