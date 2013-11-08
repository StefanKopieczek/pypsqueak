cat stats.txt | sed -e 's/\(^. \)[0-9]\+ /\1/g' > stats-no-length.txt
