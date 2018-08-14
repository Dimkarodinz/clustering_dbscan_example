from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()
celery_logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(hour=settings.CLUSTERING_HOURS, minute=0)),
    name="clusterize_users",
    ignore_result=True
)
def clusterize_users():
    # todo: make as factory, incapsulate to classes
    _classes = (Interest, Cause, Skill)

    for _class in _classes:
        groupped_users = User.objects.grouping_by(_class)
        celery_logger.info("User clusterization for %s was inited" % _class.__name__)

        if groupped_users:
            for group in groupped_users:

                is_add_interests = False
                if _class is Interest:
                    is_add_interests = True

                celery_logger.info("Clusterization for group %s was started" % group['name'])

                normalized_data, user_ids = cluster.clustering_normalize(group['objects'])

                labels, idx = cluster.clusterize(normalized_data)
                grouped_infos = cluster.clustering_denormalize(
                                                source_data=user_ids,
                                                labels=labels,
                                                indicies=idx)

                grouped_locations = cluster.clustering_denormalize(
                                                source_data=normalized_data,
                                                labels=labels,
                                                indicies=idx)

                for cluster_info in grouped_infos:
                    label_info = cluster_info['label']
                    user_ids = cluster_info['payload']

                    _cluster_locations = [lab['payload'] for lab in grouped_locations
                                          if lab['label'] == label_info]

                    cluster_center = cluster.get_center(_cluster_locations)

                    # ******* Create required models ************
                    celery_logger.info("Creating database entities for %s" % label_info)
                    party = Party.objects.create_auto()

                    interests = []
                    if is_add_interests:
                        _i = Interest.objects.get(name=group['name'])
                        interests.append(_i)

                    party_occurence = PartyOccurence.objects.create_auto(
                                        info=label_info,
                                        party=party,
                                        o_name=group['name'],
                                        interests=interests)

                    v_lat, v_lng, v_address, v_name = get_foursquare_venue(
                                                        lat=cluster_center[0],
                                                        lng=cluster_center[1],
                                                        category_query=group['name'])

                    _ = PartyLocation.objects.create_auto(lat=v_lat,
                                                          lng=v_lng,
                                                          occurence=party_occurence,
                                                          address=v_address,
                                                          venue_name=v_name)

                    celery_logger.info("Clusterization finished")
