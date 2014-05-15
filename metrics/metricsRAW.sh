if [ $1 ]
	then
		echo "
		Calculate static metrics
		------------------------
		"
		radon raw ../. -e "*/migration/*"
	else
		mkdir result -p
		radon raw ../. -e "*/migration/*" > result/metricsRAW.txt -s
fi