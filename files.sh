graph() { cat <<-EOF
	digraph G {
		ok -> okok;
	  ok -> "101python" ;
	  ok -> "101wrap" -> "101wrapok"
  }
EOF
}

graph > /tmp/files.dot
dot -Tpdf /tmp/files.dot -o files.pdf