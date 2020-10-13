from posts.models import Post
from groups.models import *
from pfe import settings

def RandomPorjects():
    np = Post.objects.count()
    nf = FicheDeVoeux.objects.count()
    d = round(nf/np)
    queryFiche = FicheDeVoeux.objects.all()
    queryPost = Post.objects.all()
    for group in queryFiche:
        choosed_group = random.choice(queryFiche)
        for i in range(settings.MAXCHOICES):
          for post in queryPost:
               if post == choosed_group.choices[i] and d > post.project_choice_count():
                    choosed_group.selected_project = post
                    queryFiche.exclude(groupfiche=group.groupfiche)
                    if d <= post.project_choice_count():
                        queryPost.exclude(groupfiche=group.groupfiche)
                    break
                else:
                    continue

    if (queryFiche != Null and queryPost == Null):
        queryPost2 = Post.objects.all()
        for group in queryFiche:
            choosed_group = random.choice(queryFiche)
            for i in range(settings.MAXCHOICES):
                for post in queryPost2:
                    if post == choosed_group.choices[i]:
                        choosed_group.selected_project = post
                        queryFiche.exclude(groupfiche=group.groupfiche)
                        queryPost2.exclude(groupfiche=group.groupfiche)
                        break
                    else:
                        continue