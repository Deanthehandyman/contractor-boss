[app]
title = Contractor BOSS
package.name = contractor_boss
package.domain = org.contractorboss
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,spec
version = 1.0.0
requirements = python3,kivy,pillow,pytesseract,sqlite3
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True
android.arch = arm64-v8a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
