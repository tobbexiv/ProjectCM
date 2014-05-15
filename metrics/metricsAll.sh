if [ $2 ]
	then cd ../metrics/
fi

if [ $1 ]
	then
		echo "
		Metrics
		=======

		See http://radon.readthedocs.org for more information on radon.
		"
		bash metricsCC.sh console
		bash metricsMI.sh console
		bash metricsRAW.sh console
	else
		bash metricsCC.sh
		bash metricsMI.sh
		bash metricsRAW.sh
fi