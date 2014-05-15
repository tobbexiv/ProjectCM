if [ $1 ]
	then
		echo "
		Calculate ciclomatic complexity
		-------------------------------
		"
		radon cc ../. -e "*/migration/*"
	else
		mkdir result -p
		radon cc ../. -e "*/migration/*" > result/metricsCC.txt --total-average -s
fi