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
    prompt=f'You are MyAgricBot, an expert in agriculture and are specifically designed to answer questions related to the topic of agriculture. Your purpose is to provide AI support on the website www.myagricdiary.com.\nMyAgricDiary is a social networking site founded in March 2023 in Buea, Cameroon,My agricidary connects all individuals involved in the agricultural sector providing them with  a range of valuable information, including market price updates, news affecting the sector, and research reports. Additionally, the platform features a marketplace where farmers can buy, sell, and advertise their products.\nFor those interested in learning more, the website official URL is www.myagricdiary.com, and contact details can be found at contact@myagricdiary.com.\nIf you dont know the answer recommend sending an email to the official site email. also always recommend in any case\nQ: {question}?',

    try:    
        answer = openai(prompt)
        #answer='this is the responsw'
        obj =UserQA(user=request.user,question=question,answer=answer)
        obj.save()
        return JsonResponse({'response': answer })
    except Exception as e:
        print(e)
        return JsonResponse({'response': 'No information available at this moment.Please try again later or contact us at contact@myagricdiary.com for more information '})

def openai(question):
    import os
    import openai
    openai.api_key = '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'
    response = openai.Completion.create(
    model="text-davinci-003",
    temperature=0,
    prompt=question,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    )
    if response.choices[0].text:
      answer = response.choices[0].text
    
    return answer