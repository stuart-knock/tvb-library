# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2013, Baycrest Centre for Geriatric Care ("Baycrest")
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Environment related checks or operations are to be defined here.

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
.. moduleauthor:: Mihai Andrei <mihai.andrei@codemart.ro>
"""

import os
import sys

class Environment():

    IS_WORK_IN_PROGRESS = os.environ.get('TVB_WIP', False) == 'True'

    def is_framework_present(self):
        """
        :return: True when framework classes are present and can be imported.
        """
        framework_present = True
        try:
            from tvb.config.profile_settings import WebSettingsProfile
        except ImportError:
            framework_present = False

        return framework_present


    @staticmethod
    def is_development():
        """
        Return True when TVB is used with Python installed natively.
        """
        try:
            import tvb_bin
            bin_folder = os.path.dirname(os.path.abspath(tvb_bin.__file__))
            tvb_version_file = os.path.join(bin_folder, "tvb.version")
            if os.path.exists(tvb_version_file):
                return False
            return True
        except ImportError:
            return True


    def is_linux_deployment(self):
        """
        Return True if current run is not development and is running on Linux.
        """
        return self.is_linux() and not self.is_development()


    def is_mac_deployment(self):
        """
        Return True if current run is not development and is running on Mac OS X
        """
        return self.is_mac() and not self.is_development()


    def is_windows_deployment(self):
        """
        Return True if current run is not development and is running on Windows.
        """
        return self.is_windows() and not self.is_development()


    def is_linux(self):
        return not self.is_windows() and not self.is_mac()


    @staticmethod
    def is_mac():
        return sys.platform == 'darwin'


    @staticmethod
    def is_windows():
        return sys.platform.startswith('win')


    def get_library_folder(self, default_mac):
        """
        Return top level library folder. Will be use for setting paths
        """
        if self.is_windows_deployment():
            return os.path.dirname(sys.executable)
        if self.is_mac_deployment():
            return os.path.dirname(default_mac)
        if self.is_linux_deployment():
            return os.path.dirname(sys.executable)


    def setup_tk_tcl_environ(self, root_folder):
        """
        Given a root folder to look in, find the required configuration files for TCL/TK and set the proper
        environmental variables so everything works fine in the distribution package.

        :param root_folder: the top folder from which to start looking for the required configuration files
        """
        tk_folder = self._find_file('tk.tcl', root_folder)
        if tk_folder:
            os.environ['TK_LIBRARY'] = tk_folder

        tcl_folder = self._find_file('init.tcl', root_folder)
        if tcl_folder:
            os.environ['TCL_LIBRARY'] = tcl_folder


    def _find_file(self, target_file, root_folder):
        """
        Search for a file in a folder directory. Return the folder in which the file can be found.

        :param target_file: the name of the file that is searched
        :param root_folder: the top lever folder from which to start searching in all it's subdirectories
        :returns: the name of the folder in which the file can be found
        """
        for root, _, files in os.walk(root_folder):
            for file_n in files:
                if file_n == target_file:
                    return root


    def setup_python_path(self, *paths):
        """
        Set PYTHONPATH
        :param paths: list of absolute folder paths to join.
        """
        os.environ['PYTHONPATH'] = os.pathsep.join(paths)


    def append_to_path(self, *paths):
        """
        Set PATH
        :param paths: list of absolute folder paths to join and add BEFORE the current PATH
        """
        paths = list(paths)
        paths.append(os.environ.get('PATH', ''))
        os.environ['PATH'] = os.pathsep.join(paths)
