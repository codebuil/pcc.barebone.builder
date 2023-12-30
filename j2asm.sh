printf "\ec\e[43;36m\a\n\n"
gcj -S $1 -o /tmp/temp
cat /tmp/temp
