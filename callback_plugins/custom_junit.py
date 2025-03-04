from ansible.plugins.callback.junit import CallbackModule as JunitCallbackModule

import os
import re

class CallbackModule(JunitCallbackModule):
    CALLBACK_NAME = 'custom_junit'

    def __init__(self):
        super(CallbackModule, self).__init__()

        # Enforce our own defaults for when ENVVARs are inconvenient
        self._output_dir = os.getenv('JUNIT_OUTPUT_DIR', '/var/lib/AnsibleTests/external_files/')
        self._test_case_prefix = os.getenv('JUNIT_TEST_CASE_PREFIX', 'rhelai-validation : TEST')
        self._fail_on_ignore = os.getenv('JUNIT_FAIL_ON_IGNORE', 'true')  # this is needed because we use "ignore_errors" on assertion tasks to run as many as possible
        self._hide_task_arguments = os.getenv('JUNIT_HIDE_TASK_ARGUMENTS', 'true')

    def mutate_task_name(self, task_name):
        if len(self._test_case_prefix) > 0:
            task_name = task_name.split(self._test_case_prefix)[-1]  # remove the test prefix and everything before it
        task_name = task_name.lower()
        task_name = re.sub(r'\W', ' ', task_name)  # replace all non-alphanumeric characters (except _) with a space
        task_name = re.sub(r'(^\W*|\W*$)', '', task_name)  # trim any trailing or leading non-alphanumeric characters
        task_name = re.sub(r' +', '_', task_name)  # replace any number of spaces with _
        return task_name

    def _build_test_case(self, task_data, host_data):
        tc = super()._build_test_case(task_data, host_data)

        tc.name = self.mutate_task_name(tc.name)
        # tc.system_out = None
        # tc.system_err = None
        tc.classname = 'rhoso_rhelai_validation.' + re.sub(r'\.yaml:[0-9]+$', '', os.path.basename(task_data.path))
        return tc
