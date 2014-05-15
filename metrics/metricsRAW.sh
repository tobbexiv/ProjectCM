if [ $1 ]
	then
		echo "
		Calculate static metrics
		------------------------
		"
		radon raw ../. -e "*/migration/*" --show_complexity
	else
		mkdir result -p
		radon raw ../. -e "*/migration/*" --show_complexity > result/metricsRAW.txt
fi