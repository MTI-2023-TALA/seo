#!/bin/env sh

docker build -t seo -f Dockerfile .
docker run -d --rm -p 5000:5000 --name seo seo

if test -t 1; then
    colors=$(tput colors)
    if test -n "$colors" && test $colors -ge 8; then
        normal="$(tput sgr0)"
        green="$(tput setaf 2)"
    fi
fi

echo -e "\nYou can access the app at ${green}http://localhost:5000${normal}"
