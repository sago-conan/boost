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
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False", "fPIC=True")
    short_paths = True
    no_copy_source = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        url = "https://dl.bintray.com/boostorg/release/{}/source/boost_{}.zip".format(
            self.version, self.version.replace(".", "_"))
        tools.get(url)

    def _bootstrap(self):
        if tools.os_info.is_windows:
            cmd = os.path.join(self.source_folder, "bootstrap.bat")
        else:
            cmd = "sh {}".format(os.path.join(self.source_folder, "bootstrap.sh"))
        self.output.info("Bootstrap: {}".format(cmd))
        try:
            self.run(cmd)
        except Exception as exc:
            self.output.warn(str(exc))
            if os.path.exists("bootstrap.log"):
                self.output.warn(tools.load("bootstrap.log"))
            raise

    def build(self):
        # bootstrap
        self._bootstrap()
        # config
        pass
        # vars
        pass
        # build
        pass
