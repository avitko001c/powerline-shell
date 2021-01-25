#!/bin/sh
# https://christoph-polcin.com

[ -z "$1" ] && r="origin" || r="$1"

[ "$1" = "-h" ] || [ "$1" = "--help" ] || [ ! -d ".git/refs/remotes/$r" ] && echo "usage: $(basename $0) [remote]" && exit 1

if ! git config --get remote.${r}.fetch | grep -cq refs/pull
then
	git config --add remote.${r}.fetch "'+refs/pull/*/head:refs/remotes/$r/pr/*'"
fi
git fetch $r

