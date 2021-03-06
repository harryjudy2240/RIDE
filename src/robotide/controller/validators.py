#  Copyright 2008-2015 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

from robotide.publish.messages import RideInputValidationError

ERROR_ILLEGAL_CHARACTERS = "Filename contains illegal characters"
ERROR_EMPTY_FILENAME = "Empty filename"
ERROR_NEWLINES_IN_THE_FILENAME = "Newlines in the filename"
ERROR_FILE_ALREADY_EXISTS = "File %s already exists"

class BaseNameValidator(object):

    def __init__(self, new_basename):
        self._new_basename = new_basename

    def validate(self, context):
        # Try-except is needed to check if file can be created if named like this, using open()
        # http://code.google.com/p/robotframework-ride/issues/detail?id=1111
        try:
            name = '%s.%s' % (self._new_basename, context.get_format())
            filename = os.path.join(context.directory, name)
            if self._file_exists(filename):
                RideInputValidationError(message=ERROR_FILE_ALREADY_EXISTS % filename).publish()
                return False
            if '\\n' in self._new_basename or '\n' in self._new_basename:
                RideInputValidationError(message=ERROR_NEWLINES_IN_THE_FILENAME).publish()
                return False
            if len(self._new_basename.strip()) == 0:
                RideInputValidationError(message=ERROR_EMPTY_FILENAME).publish()
                return False
            try:
                open(name,"w").close()
            finally:
                os.remove(name)
            return True
        except (IOError, OSError):
            RideInputValidationError(message=ERROR_ILLEGAL_CHARACTERS).publish()
            return False

    def _file_exists(self, filename):
        return os.path.exists(filename)
