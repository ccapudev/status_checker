import json
import requests
from django.db import models
from django.db.models import F, ExpressionWrapper, DateTimeField, Q
from django.utils import timezone
from celery import shared_task
from .models import WebService, Checkpoint, CheckpointErrors
import traceback


@shared_task
def checker_beat():
    services_to_check = WebService.objects.annotate(
        diff_date=ExpressionWrapper(
            F('last_check')+(timezone.timedelta(minutes=1)*F('minutes')),
            output_field=DateTimeField()
        )
    ).filter(
        Q(diff_date__lte=timezone.now()) | 
        Q(last_check__isnull=True)
    )
    services_to_check_count = services_to_check.count()
    for service in services_to_check:
        check_uri.delay(service.id, service.url)
    return "This task send {} Services".format(
        services_to_check_count
    )

@shared_task
def check_uri(service_id=None, url=None):
    service = None
    if service_id:
        service = WebService.objects.get(id=service_id)
        url = service.url
    if url:
        try:
            rq = requests.get(service.url, timeout=(1, 2.5))
            checkpoint = Checkpoint(
                web_service_id=service_id,
                url=rq.url,
                status_code=rq.status_code,
                reason=rq.reason,
                content_type=rq.headers.get('Content-Type', 'no-content-type'),
                body=rq.content.decode('utf8'),
                headers=json.dumps(dict(rq.headers), indent=4, sort_keys=True),
                response_time=str(rq.elapsed.total_seconds())
            )
            checkpoint.save()
            if rq.status_code > 499:
                raise ValueError("Webservice has Critical Error {}: Checkpoint: {}".format(
                    rq.status_code,
                    checkpoint.id,
                ))
            elif rq.status_code > 399:
                raise ValueError("Webservice return Error {}: Checkpoint: {}".format(
                    rq.status_code,
                    checkpoint.id,
                ))
            elif rq.status_code > 299:
                raise ValueError("Webservice Redirect {}: Checkpoint: {}".format(
                    rq.status_code,
                    checkpoint.id,
                ))
            if service:
                service.last_check = timezone.now()
        except Exception as e:
            reason=str(e)
            traceback_log=traceback.format_exc()
            CheckpointErrors(
                web_service_id=service_id,
                url=url,
                reason=reason,
                traceback_log=traceback_log,
            ).save()
    if service:
        service.save()


@shared_task
def clear_old_registers(days):
    limit_date = timezone.now() - timezone.timedelta(days=days)
    Checkpoint.objects.filter(date_request__lt=limit_date).delete()
    CheckpointErrors.objects.filter(
        date_request__lt=limit_date, archived=True
    ).delete()