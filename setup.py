from distutils.core import setup
from distutils.extension import Extension


krawczyk = Extension(name = 'hikmot.krawczyk',
                     sources = ['cpp_src/krawczyk.cc'],
                     include_dirs = ['cpp_src', '/opt/local/include','/usr/include'],
                     extra_compile_args=['-O3', '-DNDEBUG', '-fpic']
                     )

setup( name = 'hikmot',
       version = '1.0.1',
       install_requires = ['snappy'],
       packages = ['hikmot'],
       package_dir = {'hikmot' : 'python_src'},
       ext_modules = [krawczyk],
       author = 'N. Hoffman, K. Ichihara, M. Kashiwagi, H. Masai, S. Oishi, and A. Takayasu',
       author_email = 'hikmot@oishi.info.waseda.ac.jp',
       description = 'Verifed computions of hyperbolic 3-manifold structures',
       license = 'GPL',
       url = 'http://www.oishi.info.waseda.ac.jp/~takayasu/hikmot/',
       )
