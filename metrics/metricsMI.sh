if [ $1 ]
	then
		echo "
		Check maintainability
		---------------------
		"
		radon mi ../. -e "*/migration/*"
	else
		mkdir result -p
		radon mi ../. -e "*/migration/*" > result/metricsMI.txt
fi