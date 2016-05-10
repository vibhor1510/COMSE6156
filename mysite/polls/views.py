from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.db import connection
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.template import RequestContext, loader
import random
from datetime import datetime
import time

from .models import Question, Choice

from .models import Document
from .forms import DocumentForm

uId = 0
b = 0;

def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  start=time.time();
  try:
    conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    conn = None


def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  elapse = time.time()-start;
  print elapse;
  try:
    conn.close()
  except Exception as e:
    pass

def login(request):
    print "login";
    b = time.time()
    template_name = 'polls/login.html'
    print('request login')
    error = None
    print (str(request.method))
    if request.method == 'POST':
        
        query =  "SELECT * FROM users WHERE u_name=%s and u_password=%s;"
      
        cursor = connection.cursor()
        cursor.execute(query, (request.POST.get('username'),request.POST.get('password')))
        number = 0
        username = ''
        userId = 0
        for result in cursor:
            print('found')
            number=number+1
            username = result[1]
            userId = result[0]
            uId = userId
        cursor.close()
        print(number)
        if number==0:
            error = 'User not found'
        elif number>1:
            error = 'Multiple users found'
        else:
            query = "SELECT count(*) FROM ban WHERE u_id=%s"
            data = (userId,)          
            cursor = connection.cursor()
            cursor.execute(query,data)
            record = cursor.fetchone()
            if(record[0] != 0):
                 error = 'User banned'
                 messages.error(request, error)
            else:
                 #Check if admin
                 query =  "SELECT COUNT(*) FROM admin WHERE u_id=%s;"
                 data = (userId,)
                 cursor.execute(query,data)
                 record = cursor.fetchone()
                 
                 return HttpResponseRedirect('/polls/all')
                 
                 
    c = time.time()-b;
    print c*100;
    
    a = time.time();
    return render_to_response('polls/login.html', RequestContext(request))
    l=time.time()-a;
    print l;

def all(request):
    print "loading posts"
    b=time.time();
    query =  'SELECT * \
                FROM question_posted ORDER BY q_date DESC;'
    cursor = connection.cursor()
    cursor.execute(query)
    questions = cursor.fetchall()
    cursor.close()
    template = loader.get_template('polls/all.html')
    context = { 'questions': questions }
    print (time.time()-b);
    d = time.time();
    return HttpResponse(template.render(context, request))
    r = time.time() - d;
    print r;   
 
def signup(request):
   print "signup"
   b=time.time();
   print (time.time()-b)*10000;
   d = time.time();
   template_name = 'polls/signup.html'
   return render_to_response('polls/signup.html')
   r = time.time() - d;
   print r; 

def signupclick(request):
   u_name = request.POST.get('User name')
   u_password = request.POST.get('Password')
   cursor = connection.cursor()
   query = "SELECT * FROM Users"
   cursor.execute(query)
   exists = False
   for row in cursor:
    if(row[1] == u_name):
      exists = True
   if (u_name == ""):
     message = "No user name entered, cannot sign up"
     return message
   if (u_password == ""):
     message = "No password entered, cannot sign up"
     return message;
   if (exists == False):
    query = "INSERT INTO Users (U_NAME,U_PASSWORD) VALUES (%s,%s)"
    data = (u_name,u_password,)
    cursor.execute(query,data)
    message = "Signed up successfully"
    print message
   else:
    message = "This user name already exists, try a different one"
   return HttpResponse(message)

def logout(request):
    messages.add_message(request, messages.INFO, 'You were logged out.')
    return render_to_response('polls/login.html', RequestContext(request))

def addQuestion(request):
  print "addQuestion"
  b=time.time();
  text = request.POST.get('text')
  userIdentity = 1 
  query = "INSERT INTO question_posted (u_id, q_text,q_date) VALUES (%s, %s ,%s)"
  data = (userIdentity, text, datetime.now())
  #query = "INSERT INTO question_posted (u_id, q_text,q_date) VALUES (%s,%s,now())"
    #data = (session['userId'],text)
  cursor = connection.cursor()
  cursor.execute(query,data)
  print (time.time()-b)*100;
  return HttpResponseRedirect('/polls/all')
  #return redirect('/all')

def CommentUnfold(Tree,Hashlist,CommentList,deepness):
    for i in Tree:
        CommentList.append((i,deepness))
        CommentUnfold(Hashlist[str(i[0])],Hashlist,CommentList,deepness+1)

def posting(request, id="1"):
    info = request.GET.get('id', '')#id is passed in the request arguments in the URL
    pid = int(id)

    query =  'SELECT count(*) \
              FROM question_posted q, excited e \
              WHERE q.q_id=%s AND q.q_id=e.q_id;'
    cursor = connection.cursor()
    cursor.execute(query,(pid,))
    record = cursor.fetchone()
    excite = record[0]
    cursor.close()

    #has the user liked it before
    query =  'SELECT count(*) \
              FROM question_posted q, excited e \
              WHERE q.q_id=%s AND q.q_id=e.q_id AND e.u_id=%s;'
    cursor = connection.cursor()
    cursor.execute(query,(pid, 1,)) # HC Verma
    record = cursor.fetchone()
    userExcited = (record[0]==1)
    cursor.close()

    #get the text for the question
    query =  'SELECT * \
              FROM question_posted q, users u \
              WHERE q.q_id=%s AND q.u_id=u.u_id;'
    cursor = connection.cursor()
    cursor.execute(query,(pid,))
    record = cursor.fetchone()
    question = {'text':record[2],'date':record[3],'excite':excite,'id':pid, 'u_id':record[4], 'u_name':record[5]}
    print question
    cursor.close()

    #get the answers text and votes for the question
    query =  'select agg.q_id,agg.a_text,agg.a_id,count(v.a_id) c,agg.a_date,agg.u_id,agg.u_name\
              FROM vote v\
              RIGHT JOIN\
              (SELECT a.a_id,a.q_id,a.u_id,a.a_text,a.a_date,u.u_name FROM question_posted q, answer_proposed a, users u\
              WHERE q.q_id=%s AND q.q_id=a.q_id AND u.u_id=a.u_id) agg\
              ON agg.a_id=v.a_id\
              GROUP BY agg.a_id,agg.q_id,agg.u_id,agg.a_text,agg.a_date,agg.u_name\
              ORDER BY c DESC;'
    cursor = connection.cursor()
    cursor.execute(query,(pid,))
    answers = []
    total = 0.
    for result in cursor:
      answers.append((result[1],result[3],result[2],result[4], result[5],result[6]))  
      total += result[3]
    cursor.close()

    #get the user's vote choice
    query =  'SELECT a.a_id, v.v_date\
              FROM question_posted q, answer_proposed a, vote v\
              WHERE q.q_id=%s AND q.q_id=a.q_id AND a.a_id=v.a_id AND v.u_id=%s;'
    cursor = connection.cursor()
    cursor.execute(query,(pid, 1)) # HC Verma
    record = cursor.fetchone()
    print(record!=None)
    print(record)
    #print((pid,session['userId']))
    vote = [record!=None,0]
    if(vote[0]):
      vote[1]=tuple(record)
    cursor.close()

    #get the comments for the question, displayed in Chronological per deepness order
    query =  'SELECT BIG.c_id,BIG.c_parent_id,BIG.u_id,BIG.c_text,BIG.c_date,BIG.u_name,BIG.c,count(P.u_id) b FROM\
              (SELECT agg.c_id,agg.c_parent_id,agg.u_id,agg.c_text,agg.c_date,agg.u_name,count(L.u_id) c FROM\
              (SELECT c.c_id,c.c_parent_id,c.u_id,c.c_text,c.c_date, u.u_name\
              FROM question_posted q, comment_added c, users u\
              WHERE c.q_id=q.q_id AND q.q_id=%s AND c.u_id=u.u_id) agg\
              LEFT JOIN\
              (SELECT * FROM LIKES WHERE u_id=%s) L\
              ON agg.c_id=L.c_id\
              GROUP BY agg.c_id,agg.c_parent_id,agg.u_id,agg.c_text,agg.c_date,agg.u_name) big\
              LEFT JOIN\
              LIKES P\
              ON big.c_id=P.c_id\
              GROUP BY BIG.c_id,BIG.c_parent_id,BIG.u_id,BIG.c_text,BIG.c_date,BIG.u_name,BIG.c\
              ORDER BY big.c_date ASC, c_id ASC;'
    cursor = connection.cursor()
    cursor.execute(query,(pid, 1))
    commentsTree = []
    commentHash = {'root':commentsTree}
    for result in cursor:#chronological order assumed from the query 
      selfId=result[0]
      parentId=result[1]
      newTree=[]
      parent=commentsTree
      if(parentId!=1):
        parent=commentHash[str(parentId)]
      parent.append(result)
      commentHash[str(selfId)]=newTree
    commentsList=[]
    CommentUnfold(commentsTree,commentHash,commentsList,0)
    cursor.close()
    #return render_to_response('polls/Jin.html', vote=vote, userExcited=userExcited, comments=commentsList, total=total, answers=answers, question=question)
    #return render_to_response('polls/signup.html')
    template = loader.get_template('polls/Jin.html')
    context = { 'vote': vote, 'userExcited': userExcited, 'comments':commentsList, 'total':total, 'answers':answers,'question':question }
    return HttpResponse(template.render(context, request))

def likeComment(request, pid="1", cid="1"):
    cid = int(cid)
    pid = int(pid)
    print pid, cid
    cursor = connection.cursor()
    cursor.execute('INSERT INTO likes VALUES (%s,%s)', (1 ,cid,)) # HC Verma
    return HttpResponseRedirect('/polls/posting/'+str(pid))

def UnlikeComment(request, pid="1", cid="1"):
    cid = int(cid)
    pid = int(pid)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM likes WHERE u_id=%s AND c_id=%s;', (1,cid,)) # HC Verma
    return HttpResponseRedirect('/polls/posting/'+str(pid))

def likePost(request, id="1"):
    print "likePost";
    b = time.time();
    pid = int(id)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO excited VALUES (%s,%s)', (1, pid,)) # HC Verma
    print time.time()-b;
    return HttpResponseRedirect('/polls/posting/'+str(pid))

def UnlikePost(request, id="1"):
    pid = int(id)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM excited WHERE u_id=%s AND q_id=%s;', (1,pid,)) # HC Verma
    return HttpResponseRedirect('/polls/posting/'+str(pid))

def votePost(request, pid="1", aid="1"):
    pid = int(pid)
    aid = int(aid)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO vote VALUES (%s,%s,now())', (1,aid,))
    return HttpResponseRedirect('/polls/posting/'+str(pid))

def unvotePost(request, pid="1", aid="1"):
    pid = int(pid)
    aid = int(aid)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM vote WHERE u_id=%s AND a_id=%s;', (1,aid,))
    return HttpResponseRedirect('/polls/posting/'+str(pid))

def addAnswer(request, id="1"):
    pid = int(id)
    text = request.POST.get('text')
    query = "INSERT INTO answer_proposed (q_id,u_id,a_text,a_date) VALUES (%s,%s,%s,now())"
    data = (pid, 1,text) # HC Verma
    cursor = connection.cursor()
    cursor.execute(query,data)
    return HttpResponseRedirect('/polls/posting/'+str(pid))

def addCommentRoot(request, id="1"):
    pid = int(id)
    text = request.POST.get('text')
    query = "INSERT INTO comment_added (c_parent_id,u_id,q_id,c_text,c_date) VALUES (1,%s,%s,%s,now())"
    data = (1,pid,text) 
    cursor = connection.cursor()
    cursor.execute(query,data)
    return HttpResponseRedirect('/polls/posting/'+str(pid))

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def list(request):
    # Handle file upload
    print "here"
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.owner = request.user
            b = time.time()
            newdoc.save()
            print time.time() - b;
            print "there"
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('polls:signup'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    return
    # Render list page with the documents and the form
    return render_to_response('polls/signup.html', {'documents': documents, 'form': form},context_instance=RequestContext(request))
    
