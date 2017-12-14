import requests
import vk
import asyncio

import settings as ss
import logging

logging.basicConfig(format="[%(thread)-5d]%(asctime)s: %(message)s")
loop = asyncio.get_event_loop()  # event loop


def auth():
    """
    Just auth for VK Api
    :return:
    """
    logging.info("Try to authenticate...")
    session = vk.Session(access_token=ss.TOKEN)
    vk_api = vk.API(session)
    return vk_api


async def download_members(url):
    try:
        info = requests.post(url).json()
        logging.info("Try to get info...")
        return info
    except requests.exceptions.RequestException as error:
        logging.error("Occurred ", error.strerror)
        return error


async def mem_worker(urls):
    info = await asyncio.gather(*[download_members(l) for l in urls])
    members = []
    for block in info:
        members += block.get('response', 'empty')

    return members


def get_members_asy(group_id, group_len, fields=ss.MEMBERS_FIELDS):
    """
    :param group_len: Members count
    :param fields: For example - sex,b_date,city.
    :param group_id: Group name.
    :return: info ( uses fields ) about all users in group
    """
    logging.info("Try to get members from..." + group_id)
    members = None # List for members info.
    proc_name = "getAllMembers"  # Name of stored procedure in VK app

    # Fields, which we can get from users.
    fields_arg = "&fields={0}".format(fields)
    token_arg = "?access_token={0}".format(ss.TOKEN)
    group_arg = "&groupLen={0}".format(group_len)
    id_arg = "&groupId={0}".format(group_id)

    # Concatenate all together and get link to post request
    post_url = ss.BASE_URL + proc_name + token_arg + fields_arg + group_arg + id_arg
    if group_len == 0:
        logging.debug("Group ", group_id, " has no members.")
        return None

    urls = [post_url + "&membersLen={0}".format(l if l < group_len else group_len)
            for l in range(0, group_len + 25_000, 25_000)]
    members = loop.run_until_complete(mem_worker(urls))
    print(members)

    return members


def get_members(group_id, group_len, fields=ss.MEMBERS_FIELDS):
    """
       :param group_len: Members count
       :param fields: For example - sex,b_date,city.
       :param group_id: Group name.
       :return: info ( uses fields ) about all users in group
    """
    logging.info("Try to get members from..." + group_id)
    members = []  # List for members info.
    proc_name = "getAllMembers"  # Name of stored procedure in VK app

    # Fields, which we can get from users.
    fields_arg = "&fields={0}".format(fields)
    token_arg = "?access_token={0}".format(ss.TOKEN)
    group_arg = "&groupLen={0}".format(group_len)
    id_arg = "&groupId={0}".format(group_id)

    # Concatenate all together and get link to post request
    post_url = ss.BASE_URL + proc_name + token_arg + fields_arg + group_arg + id_arg
    if group_len == 0:
        logging.debug("Group ", group_id, " has no members.")
        return None

    # We get the data about the users until we get everything (25 000 users for one cycle)
    while len(members) < group_len:
        proc_args = "&membersLen={0}".format(len(members))
        try:
            info = requests.post(post_url + proc_args).json()
        except requests.exceptions.RequestException as error:
            logging.error("Occurred ", error.strerror)
            return error

    # Use the get() method to avoid use try/catch for KeyError exception
        members += info.get('response', 'empty')
        logging.debug("Get members:" + str(len(members)) + " from " + group_id)

    return members


def get_posts_asy(group_id, wall_len):
    logging.info("Try to get posts from..." + group_id)
    proc_name = "getAllPosts"
    domain_arg = "&domain={0}".format(group_id)
    token_arg = "?access_token={0}".format(ss.TOKEN)
    wall_arg = "&wallLen={0}".format(wall_len)
    post_url = ss.BASE_URL + proc_name + token_arg + wall_arg + domain_arg

    urls = [post_url + "&postsLen={0}".format(l if l < wall_len else wall_len)
            for l in range(0, wall_len + 25_000, 25_000)]
    posts = loop.run_until_complete(mem_worker(urls))


    return posts


def get_posts(group_id, wall_len):
    logging.info("Try to get posts from..." + group_id)
    posts = []
    proc_name = "getAllPosts"
    domain_arg = "&domain={0}".format(group_id)
    token_arg = "?access_token={0}".format(ss.TOKEN)
    wall_arg = "&wallLen={0}".format(wall_len)
    post_url = ss.BASE_URL + proc_name + token_arg + wall_arg + domain_arg
    while len(posts) < wall_len:
        proc_args = "&postsLen={0}".format(len(posts))
        try:
            info = requests.post(post_url + proc_args).json()
        except requests.exceptions.RequestException as error:
            logging.error("Occurred ", error.strerror)
            return error

        posts += info.get('response', 'empty')
        logging.debug(("Get posts:" + str(len(posts)) + " from " + group_id))

    return posts


if __name__ == "__main__":
    auth()

