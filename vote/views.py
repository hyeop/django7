from django.shortcuts import render, redirect
from .models import Topic, Choice
# Create your views here.
def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        cho = request.POST.getlist("cho")
        
        t = Topic(subject=s, content=c, maker=request.user)
        t.save()
        for i in cho:
            Choice(topic=t, name=i).save()
        return redirect("vote:index")
        
    return render(request, "vote/create.html")

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        # 투표한 사람목록에 요청한사람이 없을때만 밑구문실행
        t.voter.add(request.user)
        cpk = request.POST.get("cho")
        c = Choice.objects.get(id=cpk)
        c.num += 1
        c.save()
    return redirect("vote:detail", tpk)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "t" : t,
        "cset" : c
    }
    return render(request, "vote/detail.html", context)

def index(request):
    t = Topic.objects.all()
    context = {
        "tset" : t
    }
    return render(request, "vote/index.html", context)