name: Android CI Build
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Fix Permissions
        run: sudo chmod -R 777 .

      - name: Build with Buildozer
        run: |
          docker run --rm -v $GITHUB_WORKSPACE:/home/user/hostcwd kivy/buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: ContractorBOSS-Latest
          path: bin/*.apk
