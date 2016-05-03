from django.shortcuts import render
from .forms import *
from DjangoApp.pyparse import *
# Create your views here.
from django.http import JsonResponse
from .models import *
def contact(request):

    form = ContactForm(request.POST or None)
    context = {
    "form" : form,

    }

    return render(request,"forms.html",context)

def play_count_by_month(request):
    # print(list(Node_Data.objects.all().values('name','group')))
    # print(list(Node_Relations.objects.all().values('destination_node','source_node')))

    jsondata = {
        "nodes": list(Node_Data.objects.all().values('name','group')),
        "links":list(Node_Relations.objects.all().values('source','target','value'))
    }
    print (jsondata)

    var1 = {"nodes": [
    { "name": "a", "group": 1 },
    { "name": "b", "group": 1 },
    { "name": "c", "group": 1 },
    { "name": "d", "group": 1 },
    { "name": "e", "group": 1 },
    { "name": "f", "group": 1 },
    { "name": "g", "group": 1 },
    { "name": "h", "group": 2 },
    { "name": "i", "group": 2 },
    { "name": "j", "group": 4 },
    { "name": "k", "group": 3 }
  ],
  "links": [
    { "source": 0, "target": 7, "value" : 1 },
    { "source": 1, "target": 7, "value" : 1 },
    { "source": 2, "target": 7, "value" : 1 },
    { "source": 2, "target": 8, "value" : 1 },
    { "source": 3, "target": 8, "value" : 1 },
    { "source": 4, "target": 8, "value" : 1 },
    { "source": 5, "target": 9, "value" : 1 },
    { "source": 5, "target": 10, "value" : 1 },
    { "source": 6, "target": 9, "value" : 1 },
    { "source": 7, "target": 10, "value" : 1 },
    { "source": 8, "target": 10, "value" : 1 },
    { "source": 9, "target": 10, "value" : 1 }
  ]
}
    print (var1)
    return JsonResponse(jsondata, safe=False)


def home(request):
    print (request.POST)
    form = InitialString(request.POST or None)
    title = "Welcome"
    context = {
        "template_title" :title,
        "initform" : form
    }
    node_field_form = Node_Data
    #
    #
    if form.is_valid():
        print (form.cleaned_data["input_string"])

        input_data = form.cleaned_data["input_string"]

        entry_point(input_data)
        context = {
        "template_title" :"submitted",
        "initform" : form
          }
    #     print request.POST[in]
        # print (form.input_string)
        # instance = node_field_form.save()
        # print (instance.input_string)

    return render(request,"home.html",context)