import logging, re


logger = logging.getLogger('TrackingApp')

routes_map = {'register': '{user} has just been registered',
              'login': '{user} logged in',
              'logout': '{user} logged out',
              'add': '{user} added a Todo',
              'edit': '{user} edited a Todo',
              'complete': '{user}  completed an Todo'}


def generate_log_message(user, url):
    url_split = ':'.join(re.findall(r'[A-z]+', url))
    message = '{user} has visited {page} page'.format(user=user,
                                                      page=url_split if url_split else 'home')
    return message


def log_event(request):
    if request.method == 'POST':
        print(request.POST)
        url = request.path.split('/')[-1]
        message = routes_map[url].format(user=request.user)
    else:
        message = generate_log_message(request.user, request.path)

    logger.info(message)
