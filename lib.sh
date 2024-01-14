printf "\x1bc\x1b[43;37m\n"
gcc -print-search-dirs | grep -oP 'install:\s+\K.*' > /tmp/null
paths=$(cat /tmp/null)
filename="libgcc.a"
paths="$paths$filename"
objdump  -M intel -d -S $paths | bash awk.sh
 
