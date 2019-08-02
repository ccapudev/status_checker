from django.db import models

# Create your models here.
class WebService(models.Model):
    url = models.URLField("URL")
    domain = models.CharField("Domain", max_length=200,
        blank=True, null=True)
    ip = models.GenericIPAddressField("IP", blank=True, null=True)
    last_check = models.DateTimeField(
        "Ultimo checkpoint", blank=True, null=True)
    minutes = models.PositiveIntegerField("Intervalo en minutos", default=2)
    is_active = models.BooleanField("Activo", default=True)
    slack_api = models.URLField("Slack Webhook URL", blank=True, null=True)

    def __str__(self):
        return '{}:{} cada {} min ({})'.format(
            'Activo' if self.is_active else 'Inactivo',
            str(self.url or '')[10:],
            self.minutes,
            self.last_check,
        )

    @classmethod
    def parse_url(cls, url):
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return dict(
            domain=parsed.netloc,
            ip=cls.get_ip(parsed.netloc)
        )

    @classmethod
    def get_ip(cls, domain, raise_exception=False):
        import socket
        try:
            return socket.gethostbyname(domain)
        except Exception as e:
            if raise_exception:
                raise e
            return None

    def save(self, *args, **kwargs):
        try:
            parsed = self.parse_url(self.url)
            self.domain = parsed['domain']
            self.ip = parsed['ip']
        except Exception as e:
            print(e)
            pass
        super().save(*args, **kwargs)


class Checkpoint(models.Model):
    date_request = models.DateTimeField(auto_now=True, null=True)
    web_service = models.ForeignKey(
        WebService, null=True, on_delete=models.SET_NULL,
        related_name='checkpoints'
    )
    url = models.URLField("URL", blank=True, null=True)
    status_code = models.IntegerField(
        'Codigo de estado', blank=True, null=True)
    reason = models.CharField(
        'Razon de estado', blank=True, null=True, max_length=64)
    content_type = models.CharField(
        "Tipo de contenido", max_length=64, blank=True, null=True)
    body = models.TextField("Cuerpo de respuesta", blank=True, null=True)
    headers = models.TextField("Cabeceras", blank=True, null=True)
    response_time = models.DecimalField(
        "Tiempo de repuesta", decimal_places=6, max_digits=9)

    def __str__(self):
        return '{}: {}:{} - {}'.format(
            str(self.url or '')[10:],
            self.status_code,
            self.reason,
            self.content_type,
        )

    class Meta:
        verbose_name = 'Punto de control'
        verbose_name_plural = 'Puntos de control'


class CheckpointErrors(models.Model):
    date_request = models.DateTimeField(auto_now=True, null=True)
    web_service = models.ForeignKey(
        WebService, null=True, on_delete=models.SET_NULL,
        related_name='checkpoints_errors'
    )
    url = models.URLField("URL")
    reason = models.TextField("Razon", blank=True, null=True)
    traceback_log = models.TextField("Traceback", blank=True, null=True)
    archived = models.NullBooleanField(default=False)

    def __str__(self):
        return '{}: {}:{}'.format(
            str(self.url or '')[10:],
            self.reason,
            self.archived,
        )

    class Meta:
        verbose_name = 'Error de punto de control'
        verbose_name_plural = 'Errores de punto de control'