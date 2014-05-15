if [ $1 ]
	then
		echo "
		Calculate static metrics
		------------------------
		"
		radon raw ../. -e "*/migration/*" --summary
	else
		mkdir result -p
		radon raw ../. -e "*/migration/*" --summary > result/metricsRAW.txt
fi