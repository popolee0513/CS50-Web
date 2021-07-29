from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import markdown
import numpy as np


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request,title):
    if util.get_entry(title)!=None:
        return render(request, "encyclopedia/data.html", {
         "data":  markdown.markdown(util.get_entry(title)),
         "title":title
    })
        
    else:
        return render(request, "encyclopedia/data.html", {
         "data": "The page was not found!",
         "title":title
    })
def create(request):
    if request.method == "POST":
        form = request.POST.dict()
      
        title = form['title']
        content=form['comment']
        check=[x.lower()  for x in util.list_entries()]
        if title.lower() in check:
            return HttpResponse("An encyclopedia entry already exists with the provided title!")
        else:
            if len(title)!=0 and len(content)!=0 and content!="Enter text here...":
                util.save_entry(title, content)
                return HttpResponseRedirect("/wiki/"+title)
            else:
                return HttpResponse("Please provide valid input!")
                       
    else:
        return render(request, "encyclopedia/create.html")
    
def random(request):  
    ent=util.list_entries()
    ent=np.random.choice(ent)
    return HttpResponseRedirect("/wiki/"+ent)

def edit(request,title):  
    data=util.get_entry(title)
    if request.method == "POST":
        form = request.POST.dict()
      
        title = form['title']
        content=form['comment']
        util.save_entry(title, content)
        return HttpResponseRedirect("/wiki/"+title)
    else:
        return render(request, "encyclopedia/edit.html", {
        "data": data,
        "titles":title})
def search(request):  
    ans=[]
    if request.method == "POST":
        form = request.POST.dict()
      
        name= form['q']
        ent=util.list_entries()
        for i in ent:
            if name.lower()  in i.lower():
                ans.append(i)
        return render(request, "encyclopedia/index.html", {
        "entries": ans
    })
        
        
        
    
    
    
    
    
    
    
    
    
    
    