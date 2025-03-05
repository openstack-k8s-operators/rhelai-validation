from ansible.plugins.callback.junit import CallbackModule as JunitCallbackModule

import os
import re

def cleanup_name(name):
    name = name.lower()
    name = re.sub(r'\W', ' ', name)  # replace all non-alphanumeric characters (except _ an .) with a space
    name = re.sub(r' +', '_', name)  # replace any number of spaces with _
    name = re.sub(r'(^_*|_*$)', '', name)  # trim any trailing or leading _
    return name

class CallbackModule(JunitCallbackModule):
    CALLBACK_NAME = 'custom_junit'

    def __init__(self):
        super(CallbackModule, self).__init__()

        # Enforce our own defaults for when ENVVARs are inconvenient
        self._output_dir = os.getenv('JUNIT_OUTPUT_DIR', '/var/lib/AnsibleTests/external_files/')
        self._test_case_prefix = os.getenv('JUNIT_TEST_CASE_PREFIX', 'rhelai-validation : TEST')
        self._fail_on_ignore = os.getenv('JUNIT_FAIL_ON_IGNORE', 'true')  # this is needed because we use "ignore_errors" on assertion tasks to run as many as possible
        self._hide_task_arguments = os.getenv('JUNIT_HIDE_TASK_ARGUMENTS', 'true')

    def _set_class_and_name(self, tc):
        tc.classname = 'rhoso_rhelai_validation'

        if len(self._test_case_prefix) > 0 and re.search(self._test_case_prefix, tc.name):
            tc.name = tc.name.split(self._test_case_prefix)[-1]  # remove the test prefix and everything before it

            # Parse [<classname_suffix>] from begining of task name
            class_suffix_pattern = r'^\s*\[(.*?)\]'
            class_suffix_match = re.match(class_suffix_pattern, tc.name)
            if (class_suffix_match):
                tc.name = re.sub(class_suffix_pattern, '', tc.name)  # remove the class suffix tag from the name
                tc.classname += '.' + cleanup_name(class_suffix_match.group(1))

        tc.name = cleanup_name(tc.name)


    def _build_test_case(self, task_data, host_data):
        tc = super()._build_test_case(task_data, host_data)

        self._set_class_and_name(tc)
        tc.system_out = None
        tc.system_err = None
        return tc
