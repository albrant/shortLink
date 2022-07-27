from datetime import datetime, timezone

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import UrlForm
from .models import Hit, ShortUrl


def make_short_url_with_ttl(url: str, ttl: int) -> str:
    """ Функция создаёт короткую ссылку для указанной длинной ссылки,
    а также задаёт время жизни этой ссылки.
    Если ссылка уже существовала, то она обновляется
    (время жизни может поменяться)
    """
    MY_SITE = 'http://localhost:8000/'  # на боевом сервере нужно поменять
    short_url = ShortUrl.objects.get_or_create(target=url)[0]
    short_url.ttl = ttl
    short_url.save()
    return MY_SITE + short_url.key


def index(request: str) -> HttpResponse:
    """Обработчик основного адреса.
    Если пользователь уже вводил данные для создания короткой ссылки,
    то появляется созданная (или обновлённая) короткая ссылка.
    Также отрисовывается форма для ввода данных для получения новой ссылки
    """
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url')
            ttl = form.cleaned_data.get('ttl')
            url = make_short_url_with_ttl(url, ttl)
        return render(
            request,
            'shortener.html',
            {'form': form, 'url': url, 'ttl': ttl}
        )
    else:
        form = UrlForm(label_suffix='')
        return render(
            request,
            'shortener.html',
            {'form': form, 'url': ''}
        )


def redirect(request: str, key: str) -> HttpResponse:
    """Вью-функция для отработки клика по короткой ссылке:
    Проверяется, не истекло ли время жизни ссылки.
    Если не истекло, перенаправляет пользователя по длинной ссылке,
    соответствующей указанной короткой ссылке.
    Информация о клике заносится в базу данных для сбора статистики
    """
    target = get_object_or_404(ShortUrl, key=key)
    delta = datetime.now(timezone.utc) - target.added
    expired = delta.total_seconds() // 60 >= target.ttl
    if expired:  # если ссылка просрочена
        target.delete()
        return HttpResponse('Время жизни ссылки истекло. Ссылка удалена')
    try:
        hit = Hit()
        hit.target = target
        hit.referer = request.META.get("HTTP_REFERER", "")
        hit.ip = request.META.get("REMOTE_ADDR", "")
        hit.user_agent = request.META.get("HTTP_USER_AGENT", "")
        hit.save()  # записываем данные о клике по ссылке
    except IntegrityError:
        pass
    return HttpResponseRedirect(target.target)
