mkdir result -p
radon raw ../. -e "*/migration/*" > result/metricsRAW.txt -s