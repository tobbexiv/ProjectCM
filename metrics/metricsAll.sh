if [ $2 ]
	then cd ../metrics/
fi

if [ $1 ]
	then
		echo "
		Metrics
		=======
		"
		bash metricsCC.sh console
		bash metricsMI.sh console
		bash metricsRAW.sh console
	else
		bash metricsCC.sh
		bash metricsMI.sh
		bash metricsRAW.sh
fi