import boto3
import json


QUEUE_URL = 'YOUR_QUEUE_URL_HERE'


class TaskRegistry(object):

    @classmethod
    def get_task(cls, task_name):
        # Task functions are prefixed with 'task_'
        func_name = 'task_{}'.format(task_name)
        return getattr(cls, func_name)

    @classmethod
    def task_github_repositories(cls, **params):
        # Fetch number of repositories for the given user from GitHub's API
        print '{} has 5 public repositories'.format(params.get('user'))

    @classmethod
    def task_github_users(cls, **params):
        # Fetch number of user for the given city from GitHub's API
        print 'There are 1493 users in {}'.format(params.get('city'))


def lambda_handler(task, context):
    task_name = task.get('task')
    params = task.get('params')

    try:
        # Get function from registry and execute it
        func = TaskRegistry.get_task(task_name)
        func(**params)
    except:
        # Enqueue the task again if it failed
        queue = boto3.resource('sqs').Queue(QUEUE_URL)
        queue.send_message(MessageBody=json.dumps(task))

    return None
