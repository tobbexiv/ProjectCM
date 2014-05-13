mkdir result -p
radon cc ../. -e "*/migration/*" > result/metricsCC.txt --total-average -s