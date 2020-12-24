# Copyright 2018 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import logging
import os
import shutil

TAG = 'release-62-1'
VERSION= '62_1'
HASH = 'd3fa42da9aa9c2fc749fff4a31a9e57e826903681d9f4e5b4474649bf3efe271fec10f214a027d542123b85ad3f6fcfc9b6208ad3f8e4c24fe4a0cbab4024e2d'


def get(ports, settings, shared):
  if settings.USE_ICU != 1:
    return []

  ports.fetch_project('icu', 'https://github.com/unicode-org/icu/releases/download/' + TAG + '/icu4c-' + VERSION + '-src.zip', 'icu', sha512hash=HASH)
  libname = ports.get_lib_name('libicuuc')

  def create():
    logging.info('building port: icu')

    source_path = os.path.join(ports.get_dir(), 'icu', 'icu')
    dest_path = os.path.join(shared.Cache.get_path('ports-builds'), 'icu')

    shutil.rmtree(dest_path, ignore_errors=True)
    shutil.copytree(source_path, dest_path)

    final = os.path.join(dest_path, libname)
    ports.build_port(os.path.join(dest_path, 'icu4c', 'source', 'common'), final, [os.path.join(dest_path, 'icu4c', 'source', 'common')], ['--std=c++11', '-DU_COMMON_IMPLEMENTATION=1'])
    return final

  return [shared.Cache.get(libname, create)]


def clear(ports, shared):
  shared.Cache.erase_file(ports.get_lib_name('libicuuc'))


def process_args(ports, args, settings, shared):
  if settings.USE_ICU == 1:
    get(ports, settings, shared)
    args += ['-Xclang', '-isystem' + os.path.join(shared.Cache.get_path('ports-builds'), 'icu', 'source', 'common')]
  return args


def show():
  return 'icu (USE_ICU=1; Unicode License)'
