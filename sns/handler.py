import json


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


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    task_name = message.get('task')
    params = message.get('params')

    # Get function from registry
    func = TaskRegistry.get_task(task_name)

    # Execute function
    func(**params)

    return None
