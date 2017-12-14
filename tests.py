import unittest

import mock
import getters
import exceptions as exc
import time
import sys
import logging

from community import Community
from mock import patch



def get_test_members(group_id="test_community", members_count=10, debug=True, fields="sex"):
    return [{'id': 1175081, 'first_name': 'Павел', 'last_name': 'Русанов',
                'sex': 2,  'bdate': '10.7.1986', 'last_seen': {'time': 194804, 'platform': 1}},
            {'id': 5241935, 'first_name': 'Гоша', 'last_name': 'Овсянкин',
                'sex': 2, 'bdate': '10.7.1996', 'last_seen': {'time': 1517, 'platform': 2}},
            {'id': 2639698, 'first_name': 'Жанна', 'last_name': 'Дарк',
                'sex': 1, 'bdate': '13.9.1586', 'last_seen': {'time': 2534, 'platform': 3}},
            {'id': 235948,  'first_name': 'Валерия', 'last_name': 'Попова',
                'sex': 1, 'bdate': '13.9.2000', 'last_seen': {'time': 2523443, 'platform': 4}},
            {'id': 7896,    'first_name': 'Банан', 'last_name': 'Спелый',
                'sex': 'fruit', 'last_seen': {'time': 3645645, 'platform': 5}},
            {'id': 686,     'first_name': 'Чак', 'last_name': 'Паланик',
                'sex': 0, 'bdate': '10.7.2017', 'last_seen': {'time': 28493, 'platform': 6}},
            {'id': 2923838, 'first_name': 'Курлык', 'last_name': 'Курлык',
                'sex': -1, 'bdate': '10.7', 'last_seen': {'time': None, 'platform': 7}},
            {'id': 9809898, 'first_name': 'Принцесса', 'last_name': 'Лея',
                'sex': 0.5, 'bdate': '2022',
             'last_seen': {'time': -212, 'platform': 8}},
            {'id': 'qwerty', 'first_name': 'Nothing', 'last_name': 'Nothing',
             'sex': None, 'last_seen': {'time': 0, 'platform': 1}},
            {'id': None,    'first_name': 'user', 'last_name': 'user',
                'sex': 12345, 'bdate': '1.1.1999', 'last_seen': {'time': 'qwerty', 'platform': 2}}]


def get_test_posts(group_id="test_community", posts_count=5, debug=True):
    return [{'id': 0, 'marked_as_ads': 0,
             'likes': {'count': 2},
             'reposts': {'count': 16}},
            {'id': 1, 'marked_as_ads': 1,
             'likes': {'count': 0},
             'reposts': {'count': 101}},
            {'id': None,  'marked_as_ads': 0,
             'likes': {'count': 3},
             'reposts': {'count': 2},
             'views': {'count': 55}},
            {'id': -1, 'marked_as_ads': 1,
             'likes': {'count': 1},
             'reposts': {'count': 15},
             'views': {'count': 3}},
            {'id': 'qwerty', 'marked_as_ads': 0,
             'likes': {'count': 5},
             'reposts': {'count': 8},
             'views': {'count': 8}}]


def get_no_auth_vk():
    raise exc.AuthorizationError(error_data={'error_code': 5,
                                             'error_msg': 'Oops',
                                             'request_params': {},
                                             'request_uri': 'nowhere',
                                             'captcha_sid': 1010,
                                             'captch_img': None})


class TestCommunity(Community):
    def __init__(self):
        self.posts_count = 5
        self.members_count = 10
        self.group_id = "test_community"


def try_to_auth():
    try:
        getters.auth()
    except Exception:
        return False
    else:
        return True


@unittest.expectedFailure
@unittest.skipUnless(try_to_auth(), "Passed as test with аuthentication.")
class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api = getters.auth()

    @mock.patch('client.requests.get')
    def test_get_ok(self, mock_get):
        """
        Test getting a 200 OK response from the _get method of MyAPIClient.
        """
        # Construct our mock response object, giving it relevant expected
        # behaviours
        mock_response = mock.Mock()
        expected_dict = {
            "breeds": [
                "pembroke",
                "cardigan",
            ]
        }
        mock_response.json.return_value = expected_dict

        # Assign our mock response as the result of our patched function
        mock_get.return_value = mock_response

        url = 'http://api.corgidata.com/breeds/'
        # FAILED on client
        response_dict = self.client._get(url=url)

        # Check that our function made the expected internal calls
        mock_get.assert_called_once_with(url=url)
        self.assertEqual(1, mock_response.json.call_count)

        # If we want, we can check the contents of the response
        self.assertEqual(response_dict, expected_dict)


class CommunityTestCase(unittest.TestCase):
    @patch("getters.get_members", new=get_test_members)
    def test_sex_data(self):
        pub = TestCommunity()
        response = pub.sex_data()
        expected = {'Woman': 2,
                    'Man': 2,
                    'Unknown': 6}
        self.assertEqual(response, expected)
        self.assertEqual(expected['Woman'] + expected['Man'] + expected['Unknown'], pub.members_count)

    @patch("getters.get_members", new=get_test_members)
    def test_platform_data(self):
        pub = TestCommunity()
        response = pub.platform_data()
        expected = ({'Android': 1, 'Windows Phone': 1, 'Unknown': 1, 'Apple': 3},
                    {'Web': 2, 'Mobile': 2})
        self.assertEqual(response, expected)
        self.assertEqual(expected[1]['Web'] + expected[1]['Mobile'] +
                         expected[0]['Android'] + expected[0]['Windows Phone'] +
                         expected[0]['Unknown'] + expected[0]['Apple'], pub.members_count)

    @patch("getters.get_posts", new=get_test_posts)
    def test_likes_data_test(self):
        pub = TestCommunity()
        response = pub.likes_data()
        expected = {'Views': 66, 'Likes': 9, 'Likes_past': 2, 'Reposts': 25, 'Reposts_past': 117}
        self.assertEqual(response, expected)

    @patch("getters.get_members", new=get_test_members)
    def test_age_data(self):
        pub = TestCommunity()
        response = pub.age_data()
        expected = ([17], {'start': 17, 'end': 17, 'size': 2}, [31, 21], {'start': 17, 'end': 31, 'size': 2}, 7)
        self.assertEqual(response, expected)

    @unittest.expectedFailure
    def test_places_data(self):
        raise Exception

    @patch("getters.auth", new=get_no_auth_vk)
    def test_no_auth(self):
        try:
            self.api = getters.auth()
        except exc.AuthorizationError:
            pass


TIMES = 1

@unittest.skipUnless(try_to_auth(), "Passed as test with аuthentication.")
class GettersTestCase(unittest.TestCase):
    def setUp(self):
        self.api = getters.auth()

    def test_time_get_mem(self):
        com_pool = ['menmodelblog', "tnull", "potracheno", "roscosmos"]

        logging.info("Amount    |   Asyncio    |    OneThread")

        for com in com_pool:
            members_count = self.api.groups.getMembers(group_id="nomodels").get('count', 0)

            t1 = 0
            for i in range(TIMES):
                st = time.time()
                getters.get_members_asy(com, members_count)
                t1 += time.time() - st

            t1 /= TIMES

            t2 = 0
            for i in range(TIMES):
                st = time.time()
                getters.get_members(com, members_count)
                t2 += time.time() - st

            t2 /= TIMES

            logging.debug("{0}    |   {1:.5f}    |   {2:.5f}".format(members_count, t1, t2))

    def test_time_get_posts(self):
        com_pool = ['menmodelblog', "tnull", "potracheno", "roscosmos"]

        logging.info("Amount    |   Asyncio    |    OneThread")

        for com in com_pool:
            members_count = self.api.wall.get(domain=com)[0]

            t1 = 0
            for i in range(TIMES):
                st = time.time()
                getters.get_posts_asy(com, members_count)
                t1 += time.time() - st

            t1 /= TIMES

            t2 = 0
            for i in range(TIMES):
                st = time.time()
                getters.get_posts(com, members_count)
                t2 += time.time() - st

            t2 /= TIMES

            logging.debug("{0}    |   {1:.5f}    |   {2:.5f}".format(members_count, t1, t2))


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.DEBUG, filename="datahound.log")
    unittest.main()

