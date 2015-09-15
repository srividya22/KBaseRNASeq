if [ -z "$(which Rscript)" ]; then
apt-get install r-base
fi
R -q -e 'if(!require(jsonlite)) install.packages("jsonlite", repos="http://cran.us.r-project.org")'
R -q -e 'if(!require(cummeRbund)){ source("http://bioconductor.org/biocLite.R") biocLite("cummeRbund") }'
R -q -e 'if(!require(DESeq)){ source("http://bioconductor.org/biocLite.R") biocLite("DESeq")}'
R -q -e 'if(!require(edgeR)){ source("http://bioconductor.org/biocLite.R") biocLite("edgeR")}'
