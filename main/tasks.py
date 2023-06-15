'''
import requests
from . import models
from django.utils.deprecation import MiddlewareMixin

class UpdateLCGlobalDataMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response    

    def update_global_data(self):
        url = 'https://leetcode-stats-api.herokuapp.com/paulvaldez'
        response = requests.get(url)
        data = response.json()

        try:
            lc_global_data = models.LCGlobalData.objects.get(id=1)
        except models.LCGlobalData.DoesNotExist:
            lc_global_data = models.LCGlobalData(id=1)

        lc_global_data.totalQuestions = data['totalQuestions']
        lc_global_data.totalEasy = data['totalEasy']
        lc_global_data.totalMedium = data['totalMedium']
        lc_global_data.totalHard = data['totalHard']
        lc_global_data.save()

    def __call__(self, request):
        self.update_global_data()
        response = self.get_response(request)
        return response
'''