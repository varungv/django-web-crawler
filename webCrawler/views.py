from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.core.validators import URLValidator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from webCrawler.crawlerManager import CrawlerManager
from webCrawler import thread_helpers
import json


@method_decorator(csrf_exempt, name='dispatch')
class HomePageView(View):

    def get(self, request):
        return render(request, 'homePage/homePage.html', {'data': {}})

    def post(self, request):
        try:
            url = request.POST['url']
            number_of_levels = int(request.POST['numberOfLevels'])
        except Exception as e:
            req = json.loads(request.body.decode('utf-8'))
            url = req['url'][0]
            number_of_levels = int(req['numberOfLevels'][0])
        msg = ''
        try:
            validator = URLValidator()
            validator(url)
        except Exception as e:
            msg = 'Please Provide Valid URL'
            data = {'msg': msg}
        if not msg:
            crawl_manager = CrawlerManager(url, number_of_levels)
            data = {
                "links": {
                    'links': list(crawl_manager.get_links()),
                    'images': list(crawl_manager.get_images_links())
                },
                'msg': crawl_manager.msg
            }
        return JsonResponse(data)
