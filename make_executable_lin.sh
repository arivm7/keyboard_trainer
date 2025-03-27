#!/bin/bash


cd output || { echo "Не удалось прейти в папку [output]"; exit 1; }

pyinstaller -F \
--clean \
--name kb_trainer_smile \
../main.py

echo "Копирую ../books"
cp -R ../books      dist/
echo "Копирую ../saves"
cp -R ../saves      dist/
echo "Копирую ../conf.json"
cp    ../conf.json  dist/
echo "Копирую ../img"
cp -R ../img        dist/
echo "Удаляем лишнее и не понятное"
rm -R build
rm kb_trainer_smile.spec
mv dist kb_trainer_smile_lin
echo "Ок"

cd ..



# --add-data ../books:. \
# --add-data ../saves:. \
# --add-data ../conf.json:. \
# --add-binary ../img:. \


# usage: pyinstaller [-h] [-v] [-D] [-F] [--specpath DIR] [-n NAME]
#                    [--contents-directory CONTENTS_DIRECTORY]
#                    [--add-data SOURCE:DEST] [--add-binary SOURCE:DEST]
#                    [-p DIR] [--hidden-import MODULENAME]
#                    [--collect-submodules MODULENAME]
#                    [--collect-data MODULENAME] [--collect-binaries MODULENAME]
#                    [--collect-all MODULENAME] [--copy-metadata PACKAGENAME]
#                    [--recursive-copy-metadata PACKAGENAME]
#                    [--additional-hooks-dir HOOKSPATH]
#                    [--runtime-hook RUNTIME_HOOKS] [--exclude-module EXCLUDES]
#                    [--splash IMAGE_FILE]
#                    [-d {all,imports,bootloader,noarchive}]
#                    [--python-option PYTHON_OPTION] [-s] [--noupx]
#                    [--upx-exclude FILE] [-c] [-w]
#                    [--hide-console {hide-late,minimize-early,minimize-late,hide-early}]
#                    [-i <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">]
#                    [--disable-windowed-traceback] [--version-file FILE]
#                    [-m <FILE or XML>] [-r RESOURCE] [--uac-admin]
#                    [--uac-uiaccess] [--argv-emulation]
#                    [--osx-bundle-identifier BUNDLE_IDENTIFIER]
#                    [--target-architecture ARCH] [--codesign-identity IDENTITY]
#                    [--osx-entitlements-file FILENAME] [--runtime-tmpdir PATH]
#                    [--bootloader-ignore-signals] [--distpath DIR]
#                    [--workpath WORKPATH] [-y] [--upx-dir UPX_DIR] [--clean]
#                    [--log-level LEVEL]
#                    scriptname [scriptname ...]
#
# positional arguments:
#   scriptname            Name of scriptfiles to be processed or exactly one
#                         .spec file. If a .spec file is specified, most options
#                         are unnecessary and are ignored.
#
#                         Имя обрабатываемых файлов сценариев или только один файл .spec.
#                         Если указан файл .spec, большинство параметров
#                         не нужны и игнорируются.
#
#
# options:
#   -h, --help            показать это справочное сообщение и выйти
#   -v, --version         Показать информацию о версии программы и выйти.
#   --distpath DIR        Where to put the bundled app (default: ./dist)
#                         Куда поместить связанное приложение (по умолчанию: ./dist)
#   --workpath WORKPATH   Where to put all the temporary work files, .log, .pyz
#                         and etc. (default: ./build)
#                         Куда поместить все временные рабочие файлы, .log, .pyz
#                         и т.д. (по умолчанию: ./build)
#   -y, --noconfirm       Replace output directory (default:
#                         SPECPATH/dist/SPECNAME) without asking for confirmation
#                         Заменить выходной каталог (по умолчанию:
#                         SPECPATH/dist/SPECNAME) без запроса подтверждения.
#   --upx-dir UPX_DIR     Path to UPX utility (default: search the execution path)
#                         Путь к утилите UPX (по умолчанию: искать путь выполнения)
#   --clean               Clean PyInstaller cache and remove temporary files before building.
#                         Очистите кеш PyInstaller и удалите временные файлы перед сборкой.
#   --log-level LEVEL     Amount of detail in build-time console messages. LEVEL
#                         may be one of TRACE, DEBUG, INFO, WARN, DEPRECATION,
#                         ERROR, FATAL (default: INFO). Also settable via and
#                         overrides the PYI_LOG_LEVEL environment variable.
#
# What to generate:
#   -D, --onedir          Create a one-folder bundle containing an executable (default)
#                         Создать пакет из одной папки, содержащий исполняемый файл (по умолчанию)
#   -F, --onefile         Create a one-file bundled executable.
#                         Создайте исполняемый файл, состоящий из одного файла.
#   --specpath DIR        Folder to store the generated spec file (default: current directory)
#                         Папка для хранения сгенерированного файла спецификации (по умолчанию: текущий каталог)
#   -n NAME, --name NAME  Name to assign to the bundled app and spec file
#                         (default: first script's basename)
#                         Имя, которое нужно назначить связанному приложению и файлу спецификации
#                         (по умолчанию: базовое имя первого скрипта).
#   --contents-directory CONTENTS_DIRECTORY
#                         For onedir builds only, specify the name of the
#                         directory in which all supporting files (i.e.
#                         everything except the executable itself) will be
#                         placed in. Use "." to re-enable old onedir layout
#                         without contents directory.
#
#                         Только для сборок onedir укажите имя каталога,
#                         в котором будут размещены все вспомогательные файлы
#                         (т. е. все, кроме самого исполняемого файла).
#                         Используйте "." чтобы снова включить старый макет onedir без каталога содержимого.
#
# What to bundle, where to search:
#   --add-data SOURCE:DEST
#                         Additional data files or directories containing data
#                         files to be added to the application. The argument
#                         value should be in form of "source:dest_dir", where
#                         source is the path to file (or directory) to be
#                         collected, dest_dir is the destination directory
#                         relative to the top-level application directory, and
#                         both paths are separated by a colon (:). To put a file
#                         in the top-level application directory, use . as a
#                         dest_dir. This option can be used multiple times.
#
#                         Дополнительные файлы данных или каталоги, содержащие файлы данных,
#                         которые необходимо добавить в приложение.
#                         Значение аргумента должно иметь форму «source:dest_dir»,
#                         где source — это путь к файлу (или каталогу), который необходимо собрать,
#                         dest_dir — это каталог назначения относительно каталога приложения верхнего уровня,
#                         и оба пути разделены символом. двоеточие (:).
#                         Чтобы поместить файл в каталог приложения верхнего уровня, используйте <<.>> в качестве dest_dir.
#                         Эту опцию можно использовать несколько раз.
#
#   --add-binary SOURCE:DEST
#                         Additional binary files to be added to the executable.
#                         See the ``--add-data`` option for the format. This
#                         option can be used multiple times.
#
#                         Дополнительные двоичные файлы, которые необходимо добавить в исполняемый файл.
#                         См. параметр ``--add-data`` для формата. Эту опцию можно использовать несколько раз.
#
#   -p DIR, --paths DIR   A path to search for imports (like using PYTHONPATH).
#                         Multiple paths are allowed, separated by ``':'``, or
#                         use this option multiple times. Equivalent to
#                         supplying the ``pathex`` argument in the spec file.
#
#                         Путь для поиска импорта (например, при использовании PYTHONPATH).
#                         Допускаются несколько путей, разделенных ``':'``, или используйте эту опцию несколько раз.
#                         Эквивалентно предоставлению аргумента pathex в файле спецификации.
#
#   --hidden-import MODULENAME, --hiddenimport MODULENAME
#                         Name an import not visible in the code of the
#                         script(s). This option can be used multiple times.
#   --collect-submodules MODULENAME
#                         Collect all submodules from the specified package or
#                         module. This option can be used multiple times.
#   --collect-data MODULENAME, --collect-datas MODULENAME
#                         Collect all data from the specified package or module.
#                         This option can be used multiple times.
#   --collect-binaries MODULENAME
#                         Collect all binaries from the specified package or
#                         module. This option can be used multiple times.
#   --collect-all MODULENAME
#                         Collect all submodules, data files, and binaries from
#                         the specified package or module. This option can be
#                         used multiple times.
#   --copy-metadata PACKAGENAME
#                         Copy metadata for the specified package. This option
#                         can be used multiple times.
#   --recursive-copy-metadata PACKAGENAME
#                         Copy metadata for the specified package and all its
#                         dependencies. This option can be used multiple times.
#   --additional-hooks-dir HOOKSPATH
#                         An additional path to search for hooks. This option
#                         can be used multiple times.
#   --runtime-hook RUNTIME_HOOKS
#                         Path to a custom runtime hook file. A runtime hook is
#                         code that is bundled with the executable and is
#                         executed before any other code or module to set up
#                         special features of the runtime environment. This
#                         option can be used multiple times.
#   --exclude-module EXCLUDES
#                         Optional module or package (the Python name, not the
#                         path name) that will be ignored (as though it was not
#                         found). This option can be used multiple times.
#   --splash IMAGE_FILE   (EXPERIMENTAL) Add an splash screen with the image
#                         IMAGE_FILE to the application. The splash screen can
#                         display progress updates while unpacking.
#
# How to generate:
#   -d {all,imports,bootloader,noarchive}, --debug {all,imports,bootloader,noarchive}
#                         Provide assistance with debugging a frozen
#                         application. This argument may be provided multiple
#                         times to select several of the following options.
#
#                         Оказать помощь с отладкой зависшего приложения.
#                         Этот аргумент может быть предоставлен несколько раз для выбора нескольких из следующих параметров.
#
#
#                         - all: все три следующих варианта.
#
#                         - imports: specify the -v option to the underlying
#                           Python interpreter, causing it to print a message
#                           each time a module is initialized, showing the
#                           place (filename or built-in module) from which it
#                           is loaded.
#
#                           укажите опцию -v базовому интерпретатору Python,
#                           чтобы он печатал сообщение каждый раз при инициализации модуля,
#                           показывая место (имя файла или встроенный модуль), из которого он загружен.
#
#                           See https://docs.python.org/3/using/cmdline.html#id4.
#
#                         - bootloader: tell the bootloader to issue progress
#                           messages while initializing and starting the
#                           bundled app. Used to diagnose problems with
#                           missing imports.
#
#                           сообщите загрузчику, чтобы он выдавал сообщения о ходе выполнения
#                           при инициализации и запуске прилагаемого приложения.
#                           Используется для диагностики проблем с отсутствующим импортом.
#
#                         - noarchive: instead of storing all frozen Python
#                           source files as an archive inside the resulting
#                           executable, store them as files in the resulting
#                           output directory.
#
#                           вместо того, чтобы хранить все замороженные исходные файлы Python в виде архива
#                           внутри результирующего исполняемого файла, сохраните их как файлы в итоговом выходном каталоге.
#
#   --python-option PYTHON_OPTION
#                         Specify a command-line option to pass to the Python
#                         interpreter at runtime. Currently supports "v"
#                         (equivalent to "--debug imports"), "u", "W <warning
#                         control>", "X <xoption>", and "hash_seed=<value>". For
#                         details, see the section "Specifying Python
#                         Interpreter Options" in PyInstaller manual.
#   -s, --strip           Apply a symbol-table strip to the executable and
#                         shared libs (not recommended for Windows)
#   --noupx               Do not use UPX even if it is available (works
#                         differently between Windows and *nix)
#   --upx-exclude FILE    Prevent a binary from being compressed when using upx.
#                         This is typically used if upx corrupts certain
#                         binaries during compression. FILE is the filename of
#                         the binary without path. This option can be used
#                         multiple times.
#
# Windows and Mac OS X specific options:
#   -c, --console, --nowindowed
#                         Open a console window for standard i/o (default). On
#                         Windows this option has no effect if the first script
#                         is a '.pyw' file.
#   -w, --windowed, --noconsole
#                         Windows and Mac OS X: do not provide a console window
#                         for standard i/o. On Mac OS this also triggers
#                         building a Mac OS .app bundle. On Windows this option
#                         is automatically set if the first script is a '.pyw'
#                         file. This option is ignored on *NIX systems.
#   --hide-console {hide-late,minimize-early,minimize-late,hide-early}
#                         Windows only: in console-enabled executable, have
#                         bootloader automatically hide or minimize the console
#                         window if the program owns the console window (i.e.,
#                         was not launched from an existing console window).
#   -i <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">, --icon <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">
#                         FILE.ico: apply the icon to a Windows executable.
#                         FILE.exe,ID: extract the icon with ID from an exe.
#                         FILE.icns: apply the icon to the .app bundle on Mac
#                         OS. If an image file is entered that isn't in the
#                         platform format (ico on Windows, icns on Mac),
#                         PyInstaller tries to use Pillow to translate the icon
#                         into the correct format (if Pillow is installed). Use
#                         "NONE" to not apply any icon, thereby making the OS
#                         show some default (default: apply PyInstaller's icon).
#                         This option can be used multiple times.
#   --disable-windowed-traceback
#                         Disable traceback dump of unhandled exception in
#                         windowed (noconsole) mode (Windows and macOS only),
#                         and instead display a message that this feature is
#                         disabled.
#
# Windows specific options:
#   --version-file FILE   Add a version resource from FILE to the exe.
#   -m <FILE or XML>, --manifest <FILE or XML>
#                         Add manifest FILE or XML to the exe.
#   -r RESOURCE, --resource RESOURCE
#                         Add or update a resource to a Windows executable. The
#                         RESOURCE is one to four items,
#                         FILE[,TYPE[,NAME[,LANGUAGE]]]. FILE can be a data file
#                         or an exe/dll. For data files, at least TYPE and NAME
#                         must be specified. LANGUAGE defaults to 0 or may be
#                         specified as wildcard * to update all resources of the
#                         given TYPE and NAME. For exe/dll files, all resources
#                         from FILE will be added/updated to the final
#                         executable if TYPE, NAME and LANGUAGE are omitted or
#                         specified as wildcard *. This option can be used
#                         multiple times.
#   --uac-admin           Using this option creates a Manifest that will request
#                         elevation upon application start.
#   --uac-uiaccess        Using this option allows an elevated application to
#                         work with Remote Desktop.
#
# Mac OS specific options:
#   --argv-emulation      Enable argv emulation for macOS app bundles. If
#                         enabled, the initial open document/URL event is
#                         processed by the bootloader and the passed file paths
#                         or URLs are appended to sys.argv.
#   --osx-bundle-identifier BUNDLE_IDENTIFIER
#                         Mac OS .app bundle identifier is used as the default
#                         unique program name for code signing purposes. The
#                         usual form is a hierarchical name in reverse DNS
#                         notation. For example:
#                         com.mycompany.department.appname (default: first
#                         script's basename)
#   --target-architecture ARCH, --target-arch ARCH
#                         Target architecture (macOS only; valid values: x86_64,
#                         arm64, universal2). Enables switching between
#                         universal2 and single-arch version of frozen
#                         application (provided python installation supports the
#                         target architecture). If not target architecture is
#                         not specified, the current running architecture is
#                         targeted.
#   --codesign-identity IDENTITY
#                         Code signing identity (macOS only). Use the provided
#                         identity to sign collected binaries and generated
#                         executable. If signing identity is not provided, ad-
#                         hoc signing is performed instead.
#   --osx-entitlements-file FILENAME
#                         Entitlements file to use when code-signing the
#                         collected binaries (macOS only).
#
# Rarely used special options:
#   --runtime-tmpdir PATH
#                         Where to extract libraries and support files in
#                         `onefile`-mode. If this option is given, the
#                         bootloader will ignore any temp-folder location
#                         defined by the run-time OS. The ``_MEIxxxxxx``-folder
#                         will be created here. Please use this option only if
#                         you know what you are doing.
#   --bootloader-ignore-signals
#                         Tell the bootloader to ignore signals rather than
#                         forwarding them to the child process. Useful in
#                         situations where for example a supervisor process
#                         signals both the bootloader and the child (e.g., via a
#                         process group) to avoid signalling the child twice.
