title=${*:-"Title"}
echo $title

install() {
    brew install tidy-html5
}

(head="$title" bash head.sh
 bash tail.sh) |
 tidy5 -f errors.txt -config tidy.cfg
