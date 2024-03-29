##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.utils.translation import gettext
from rest_framework import generics
from rest_framework.response import Response

from base.api.serializers.polling_subscriber import PollingSubscriberSerializer
from base.models.polling_subscriber import PollingSubscriber


class AcknowledgePoll(generics.UpdateAPIView):
    """
       Acknowledge last poll request has been treated successfully by a subscriber
    """
    name = 'acknowledge-poll'
    serializer_class = PollingSubscriberSerializer
    required_parameter = 'last_poll_requested'

    def update(self, *args, **kwargs):
        if not self.request.data.get(self.required_parameter):
            return Response({self.required_parameter: gettext('This field is required.')})

        subscriber = PollingSubscriber.objects.get(app_name=self.request.user)
        subscriber.last_poll_requested = self.request.data['last_poll_requested']
        subscriber.save()

        serializer = self.get_serializer(subscriber)
        return Response(serializer.data)
