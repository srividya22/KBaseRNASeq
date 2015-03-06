compile_typespec \
-impl Bio::KBase::RNASeqServices::Impl \
-service Bio::KBase::RNASeqServices::Server \
-psgi RNASeqServices.psgi \
-client Bio::KBase::RNASeqServices::Client \
-js javascript/RNASeqServices/Client \
-py biokbase/RNASeqServices/Client \
RNASeqServices.spec lib
