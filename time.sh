for i in {1..1000}: 
do
	sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
	sleep 60

done
