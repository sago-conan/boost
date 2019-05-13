#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from conans import ConanFile, tools


class BoostConan(ConanFile):
    name = "boost"
    version = "1.70.0"
    license = "Boost Software License 1.0"
    url = "https://github.com/suwei-air/conan-boost"
    homepage = "https://www.boost.org/"
    description = "Boost provides free peer-reviewed portable C++ source libraries."
    settings = "os", "compiler", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_atomic": [True, False],
        "with_chrono": [True, False],
        "with_container": [True, False],
        "with_context": [True, False],
        "with_contract": [True, False],
        "with_coroutine": [True, False],
        "with_date_time": [True, False],
        "with_exception": [True, False],
        "with_fiber": [True, False],
        "with_filesystem": [True, False],
        "with_graph": [True, False],
        "with_graph_parallel": [True, False],
        "with_iostreams": [True, False],
        "with_locale": [True, False],
        "with_log": [True, False],
        "with_math": [True, False],
        "with_mpi": [True, False],
        "with_program_options": [True, False],
        "with_python": [True, False],
        "with_random": [True, False],
        "with_regex": [True, False],
        "with_serialization": [True, False],
        "with_stacktrace": [True, False],
        "with_system": [True, False],
        "with_test": [True, False],
        "with_thread": [True, False],
        "with_timer": [True, False],
        "with_type_erasure": [True, False],
        "with_wave": [True, False]
    }
    default_options = ("shared=False", "fPIC=True", "with_atomic=False",
                       "with_chrono=False", "with_container=False",
                       "with_context=False", "with_contract=False",
                       "with_coroutine=False", "with_date_time=False",
                       "with_exception=False", "with_fiber=False",
                       "with_filesystem=False", "with_graph=False",
                       "with_graph_parallel=False", "with_iostreams=False",
                       "with_locale=False", "with_log=False",
                       "with_math=False", "with_mpi=False",
                       "with_program_options=False", "with_python=False",
                       "with_random=False", "with_regex=False",
                       "with_serialization=False", "with_stacktrace=False",
                       "with_system=False", "with_test=False",
                       "with_thread=False", "with_timer=False",
                       "with_type_erasure=False", "with_wave=False")
    short_paths = True
    no_copy_source = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    @property
    def _boost_folder_name(self):
        return "boost_{}".format(self.version.replace(".", "_"))

    @property
    def _boost_folder(self):
        return os.path.join(self.source_folder, self._boost_folder_name)

    def source(self):
        # zip压缩包中的脚本无法携带执行权限
        url = "https://dl.bintray.com/boostorg/release/{}/source/{}.tar.bz2".format(
            self.version, self._boost_folder_name)
        tools.get(url)

    def _bootstrap(self):
        if tools.os_info.is_windows:
            cmd = "bootstrap.bat"
        else:
            cmd = "./bootstrap.sh"
        with tools.chdir(self._boost_folder):  # bat中未切换目录，需要在对应目录执行
            try:
                self.output.info("Bootstrap: {}".format(cmd))
                self.run(cmd)
            except Exception as exc:
                self.output.warn(str(exc))
                if os.path.exists("bootstrap.log"):
                    self.output.warn(tools.load("bootstrap.log"))
                raise

    # generate user-config.jam
    def _gen_user_config(self):
        pass

    @property
    def _build_options(self):
        options = []
        options.append("--prefix={}".format(self.package_folder))
        options.append("--build-dir={}".format(self.build_folder))
        options.append("--build-type=complete")
        options.append("-j{}".format(tools.cpu_count()))
        return options

    @property
    def _build_properties(self):
        prop = []
        # prop.append("toolset={}".format(toolset))
        prop.append(
            "link={}".format("shared" if self.options.shared else "static"))
        prop.append("threading=multi")
        prop.append("runtime-link=shared")
        return prop

    def build(self):
        # bootstrap
        self._bootstrap()
        # config
        self._gen_user_config()
        # build
        cmd = "b2 {} {} install".format(" ".join(self._build_options),
                                        " ".join(self._build_properties))
        with tools.chdir(self._boost_folder):
            self.output.info("Build: {}".format(cmd))
            self.run(cmd)
