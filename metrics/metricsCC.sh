if [ $1 ]
	then
		echo "
		Calculate ciclomatic complexity
		-------------------------------
		"
		radon cc ../. -e "*/migration/*" --total-average --show-complexity
	else
		mkdir result -p
		radon cc ../. -e "*/migration/*" --total-average --show-complexity > result/metricsCC.txt
fi