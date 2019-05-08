# -*- coding: utf-8 -*-
# Copyright 2019 New Vector Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from synapse.api.constants import EventTypes, RelationTypes
from synapse.rest.client.v1 import login, room
from synapse.rest.client.v2_alpha import relations

from tests import unittest


class RelationsTestCase(unittest.HomeserverTestCase):
    user_id = "@alice:test"
    servlets = [
        relations.register_servlets,
        room.register_servlets,
        login.register_servlets,
    ]

    def prepare(self, reactor, clock, hs):
        self.room = self.helper.create_room_as(self.user_id)
        res = self.helper.send(self.room, body="Hi!")
        self.parent_id = res["event_id"]

    def test_send_relation(self):
        channel = self._send_relation(RelationTypes.ANNOTATION, "m.reaction")
        self.assertEquals(200, channel.code, channel.json_body)

    def test_deny_membership(self):
        channel = self._send_relation(RelationTypes.ANNOTATION, EventTypes.Member)
        self.assertEquals(400, channel.code, channel.json_body)

    def _send_relation(self, relation_type, event_type):
        request, channel = self.make_request(
            "POST",
            "/_matrix/client/unstable/rooms/%s/send_relation/%s/%s/%s"
            % (self.room, self.parent_id, relation_type, event_type),
            b"{}",
        )
        self.render(request)
        return channel
