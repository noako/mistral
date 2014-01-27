# -*- coding: utf-8 -*-
#
# Copyright 2013 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest2

from mistral.utils import yaql_utils


DATA = {
    "server": {
        "id": "03ea824a-aa24-4105-9131-66c48ae54acf",
        "name": "cloud-fedora",
        "status": "ACTIVE"
    },
    "status": "OK"
}


SERVERS = {
    "servers": [
        {
            'name': 'centos'
        },
        {
            'name': 'ubuntu'
        },
        {
            'name': 'fedora'
        }
    ]
}


class YaqlTest(unittest2.TestCase):
    def test_expression_result(self):
        res = yaql_utils.evaluate("$.server", DATA)
        self.assertEqual(res, {
            "id": "03ea824a-aa24-4105-9131-66c48ae54acf",
            "name": "cloud-fedora",
            "status": "ACTIVE"
        })

        res = yaql_utils.evaluate("$.server.id", DATA)
        self.assertEqual(res, "03ea824a-aa24-4105-9131-66c48ae54acf")

        res = yaql_utils.evaluate("$.server.status = 'ACTIVE'", DATA)
        self.assertTrue(res)

    def test_wrong_expression(self):
        res = yaql_utils.evaluate("$.status = 'Invalid value'", DATA)
        self.assertFalse(res)

        res = yaql_utils.evaluate("$.wrong_key", DATA)
        self.assertIsNone(res)

        expression_str = "invalid_expression_string"
        res = yaql_utils.evaluate(expression_str, DATA)
        self.assertEqual(res, expression_str)

    def test_select_result(self):
        res = yaql_utils.evaluate("$.servers[$.name = ubuntu]", SERVERS)
        item = list(res)[0]
        self.assertEqual(item, {'name': 'ubuntu'})
