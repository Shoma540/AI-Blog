cd C:\Users\shoma\Desktop\AI-Blog

# lockファイル削除
if (Test-Path .git\index.lock) { Remove-Item .git\index.lock -Force }

git config user.email "shoma0406a@gmail.com"
git config user.name "Shoma540"
git add README.md .gitignore
git commit -m "update: README改訂、.env追加、.gitignore設定"
git push
