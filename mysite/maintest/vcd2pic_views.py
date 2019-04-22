from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import os
from .mytools.vcd2pic.vcd2pic import vcd2pic
#from profilehooks import profile
@csrf_exempt  # WTF
#@profile(filename="./v2p.stats", immediate=True, stdout=False)
def vcd2picjson(request):
	if request.method == 'POST':
		try:
			vcd_file = request.POST['vcd_file']
			retsponsedata = vcd2pic(vcd_file)
			return HttpResponse(retsponsedata)
		except Exception as exc:
			return HttpResponse(exc)
