from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
nextId = 4
topics = sorted([
  {'id':1, 'title':'routing', 'body': 'Routing is ...'},
  {'id':2, 'title':'view', 'body': 'View is ...'},
  {'id':3, 'title':'model', 'body': 'Model is ...'}
], key=lambda x: x['id'])

def HTMLTemlpate(articleTag, id=None):
  global topics
  contextUI = ''
  if id != None:
    contextUI = f'''
      <li>
        <form action="/delete/" method="POST">
          <input type="submit" value="delete">
          <input type="hidden" name="id" value="{id}">
        </form>
      </li>
      <li><a href="/update/{id}">update</a></li>
      '''
  ol = ''.join(f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>' for topic in topics)
  return f'''
  <html>
  <body>
    <h1><a href="/">Django</a></h1>
    <ul>
      {ol}
    </ul>
    {articleTag}
    <ul>
      <li><a href="/create/">create</a></li>
      {contextUI}
    </ul>
  </body>
  </html>
  '''

def index(request):
  article = '''
  <h2>Welcome</h2>
  Hello, Django
  '''
  return HttpResponse(HTMLTemlpate(article))

@csrf_exempt
def create(request):
  global topics, nextId
  if request.method == 'GET':
    article = '''
    <form action="/create/" method="POST">
      <p><input type="text" name="title" placeholder="title"></p>
      <p><textarea name="body" placeholder="body" id="" cols="30" rows="10"></textarea></p>
      <p><input type="submit"></p>
    </form>
    '''
    return HttpResponse(HTMLTemlpate(article))
  elif request.method == 'POST':
    title = request.POST['title']
    body = request.POST['body']
    newTopic = {"id":nextId, "title":title, "body":body}
    topics.append(newTopic)
    url = '/read/' + str(nextId)
    nextId += 1
    return redirect(url)

@csrf_exempt
def read(request, id):
  global topics
  article = ''.join(f'<h2>{topic["title"]}</h2>{topic["body"]}' for topic in topics if topic['id'] == int(id))
  return HttpResponse(HTMLTemlpate(article, id))

@csrf_exempt
def delete(request):
  global topics
  if request.method == 'POST':
    id = request.POST['id']
    newTopics = [topic for topic in topics if topic['id'] != int(id)]
    topics = newTopics
  return redirect('/')

@csrf_exempt
def update(request, id):
  global topics
  if request.method == 'GET':
    for topic in topics:
      if topic['id'] == int(id):
        selectedTopic = {
          "title": topic['title'],
          "body": topic['body']
        }
    article = f'''
    <form action="/update/{id}/" method="post">
      <p><input type="text" name="title" placeholder="title" value="{selectedTopic["title"]}"></p>
      <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
      <p><input type="submit"></p>
    </form>
    '''
    return HttpResponse(HTMLTemlpate(article, id))
  elif request.method == 'POST':
    title = request.POST['title']
    body = request.POST['body']
    for topic in topics:
      if topic['id'] == int(id):
        topic['title'] = title
        topic['body'] = body
    return redirect(f'/read/{id}')