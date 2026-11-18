#!/bin/bash
# pins the exact driver+browser pair this suite runs on:
#   Google Chrome 128.0.6613.138  (last official macOS 10.15 build,
#                                  dl.google.com/dl/chrome/mac/legacy10_15)
#   ChromeDriver 128.0.6613.137   (chrome-for-testing mac-x64, same major)
set -e
cd "$(dirname "$0")"

echo "1) chromedriver 128.0.6613.137"
curl -sL -o /tmp/cd.zip https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.137/mac-x64/chromedriver-mac-x64.zip
unzip -o -q /tmp/cd.zip
mv chromedriver-mac-x64/chromedriver .
chmod +x chromedriver
xattr -d com.apple.quarantine chromedriver 2>/dev/null || true
rm -rf chromedriver-mac-x64 /tmp/cd.zip
./chromedriver --version

echo "2) google chrome 128 (only when /Applications has none)"
if [ ! -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    curl -sL -o /tmp/chrome.dmg https://dl.google.com/dl/chrome/mac/legacy10_15/GGRO/googlechrome.dmg
    hdiutil attach /tmp/chrome.dmg -nobrowse -quiet
    cp -R "/Volumes/Google Chrome/Google Chrome.app" /Applications/
    hdiutil detach "/Volumes/Google Chrome" -quiet
    rm /tmp/chrome.dmg
    xattr -dr com.apple.quarantine "/Applications/Google Chrome.app" 2>/dev/null || true
fi
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version
