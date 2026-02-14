[app]
title = Contractor BOSS
package.name = contractor_boss
package.domain = org.contractorboss
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,spec
version = 1.0.0
requirements = python3,kivy,pillow,pytesseract,sqlite3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
