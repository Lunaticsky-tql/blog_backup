git add .
if [[ "$OSTYPE" == "darwin" ]]; then
    git commit -m "Backup on windows"
elif [[ "$OSTYPE" == "msys" ]]; then
    git commit -m "Backup through git bash"
else
    git commit -m "Backup on linux or OS X"
fi
git push origin main
hexo g
hexo d