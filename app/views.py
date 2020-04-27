from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re, praw
import json
from .scrapper import scrape, preProcess
from .classifier import predict, First

model_path = 'app/model/model.pth'
preload = First(model_path)
urlPattern = r'https:\/\/www.reddit.com\/r\/india\/comments\/\S+'
reddit = praw.Reddit(client_id = 'k2akqxbdeejOWw',
                    client_secret='fZtXNfuqoOv9LSjUZVEMO2vY2wc',
                     user_agent='Scrapper')

def home(request):
    if request.method=='POST':
        url = request.POST.get('url')
        if url and re.match(urlPattern, url):
            return show_results(request, url)
        else:
            return render(request, 'result.html', {})
    return render(request, 'index.html', {})

def processURL(url):
    print('0')
    scraped = scrape(url, reddit)
    if scraped == None:
        print('*')
        return None
    print('1')
    text = preProcess(scraped)
    print('2')
    flair = predict(text, preload)
    print('3')
    return flair

def show_results(request, url):
    result = processURL(url)
    if not result:
        return render(request, 'result.html', {})
    print(result)
    return render(request, 'result.html', {'result':result})

@csrf_exempt
def auto_test(request):
    if request.method == 'POST':
        txt_file = request.FILES
        result_dict = fromTxt(txt_file['upload_file'])
        json_file = json.dumps(result_dict)
        response = HttpResponse(json_file, content_type = 'application/json')
        response['Content-Disposition'] = 'attachment; filename =' + 'results.json'
        return response


def fromTxt(file):
    lines = file.readlines()
    lines = [line.decode('utf-8').replace('\r\n', '') for line in lines]
    result_dict = {key:None for key in lines}
    for line in lines:
        pred = processURL(line.strip())
        result_dict[line] = pred
    return result_dict