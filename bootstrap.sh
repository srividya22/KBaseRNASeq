wget https://ccb.jhu.edu/software/tophat/downloads/tophat-2.0.14.Linux_x86_64.tar.gz
wget http://cole-trapnell-lab.github.io/cufflinks/assets/downloads/cufflinks-2.2.1.Linux_x86_64.tar.gz
wget http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.5/bowtie2-2.2.5-linux-x86_64.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fbowtie-bio%2Ffiles%2Fbowtie2%2F2.2.5%2F&ts=1435073627&use_mirror=iweb
tar -xzvf tophat-2.0.14.Linux_x86_64.tar.gz
tar -xzvf cufflinks-2.2.1.Linux_x86_64.tar.gz
mv bowtie2-2.2.5-linux-x86_64.zip\?r\=http\:%2F%2Fsourceforge.net%2Fprojects%2Fbowtie-bio%2Ffiles%2Fbowtie2%2F2.2.5%2F  bowtie2-2.2.5-linux-x86_64.zip
unzip bowtie2-2.2.5-linux-x86_64.zip
rm tophat-2.0.14.Linux_x86_64.tar.gz cufflinks-2.2.1.Linux_x86_64.tar.gz bowtie2-2.2.5-linux-x86_64.zip
