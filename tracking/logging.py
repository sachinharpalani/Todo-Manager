import logging, re


logger = logging.getLogger('TrackingApp')

routes_map = {'register': '{user} has just been registered {method} {path}',
              'login': '{user} logged in {method} {path}',
              'logout': '{user} logged out {method} {path}',
              'add': '{user} added a Todo {method} {path}',
              'edit': '{user} edited a Todo {method} {path}',
              'complete': '{user}  completed an Todo {method} {path}'}


def generate_log_message(user, url):
    url_split = ':'.join(re.findall(r'[A-z]+', url.path))
    message = '{user} has visited {page} page {method} {url}'.format(user=user,
                                                                     page=url_split if url_split else 'home',
                                                                     method=url.method,
                                                                     url=url.get_full_path())
    return message


def log_event(request):
    if request.method == 'POST':
        url = request.path.split('/')[-1]
        message = routes_map.get(url, '').format(user=request.user,
                                                 method=request.method,
                                                 path=request.get_full_path())
    else:
        message = generate_log_message(request.user, request)

    logger.info(message)
