module KBaseRNASeq{

   /* Importing datatype objects from other modules */

   /*
      reference genome id for mapping the RNA-Seq fastq file
      @id ws KBaseGenomes.Genome
   */

   typedef string genome_id;

   /*
      Id for expression sample
      @id ws KBaseExpression.ExpressionSample

   */
       typedef string ws_expression_sample_id;

   /*
        List of Expression sample ids

   */

   typedef list<ws_expression_sample_id> ws_expression_sample_ids;

   /*
      Id for KBaseAssembly.SingleEndLibrary
      @id ws KBaseAssembly.SingleEndLibrary
   */

      typedef string ws_singleEndLibrary_id;

 /*
      Id for KBaseAssembly.PairedEndLibrary
      @id ws KBaseAssembly.PairedEndLibrary
   */

      typedef string ws_pairedEndLibrary_id;

 /*
      Id for KBaseAssembly.ReferenceAssembly
      @id ws KBaseAssembly.ReferenceAssembly
   */

      typedef string ws_reference_assembly_id;


   /*
      @optional hid file_name type url remote_md5 remote_sha1
   */

   typedef structure {
       HandleId hid;
       string file_name;
       string id;
       string type;
       string url;
       string remote_md5;
       string remote_sha1;
   } Handle;


  /*
      @optional reference_name
      @metadata ws handle.file_name
      @metadata ws handle.type
      @metadata ws reference_name
   */

   typedef structure {
       Handle handle;
       string reference_name;
   } ReferenceAnnotation;


   /*

   Specification for the RNASeqFastq Metadata

    Object for the RNASeq Metadata
    @optional platform source tissue condition po_id eo_id source_id ext_source_date sample_desc
   */
   typedef structure {
       string library_type;
       string platform;
       string sample_id;
       string sample_desc;
       string title;
       string source;
       string source_id;
       string ext_source_date;
       string domain;
       genome_id ref_genome;
       list<string> tissue;
       list<string> condition;
       list<string> po_id;
       list<string> eo_id;
    }RNASeqSampleMetaData;

    /*
      Complete List of RNASeq MetaData
    */
    typedef list<RNASeqSampleMetaData> RNASeqSamplesMetaData;


 /*
 RNASeq fastq  object
     @optional  singleend_sample pairedend_sample metadata
     @metadata ws metadata.sample_id
     @metadata ws metadata.library_type
     @metadata ws metadata.platform
     @metadata ws metadata.title
     @metadata ws metadata.source
     @metadata ws metadata.source_id
     @metadata ws metadata.sample_desc
     @metadata ws metadata.tissue
     @metadata ws metadata.condition

     */

     typedef structure {
         ws_singleEndLibrary_id singleend_sample;
         ws_pairedEndLibrary_id pairedend_sample;
         RNASeqSampleMetaData metadata;
     }RNASeqSample;


/*
    list of RNASeqSamples
*/

  typedef list<RNASeqSample> RNASeqSamplesSet;

/*
  The workspace id of a RNASeqSample
  @id ws KBaseRNASeq.RNASeqSample
*/

 typedef string ws_rnaseqSample_id;


 /*
    Object for the RNASeq Alignment bam file

    @metadata ws metadata.sample_id
    @metadata ws metadata.platform
    @metadata ws metadata.title
    @metadata ws metadata.source
    @metadata ws metadata.source_id
    @metadata ws metadata.sample_desc
    @metadata ws metadata.ref_genome
    @metadata ws aligned_using;
    @metadata ws aligner_version;

    */

    typedef structure{
        string aligned_using;
        string aligner_version;
        Handle handle1;
 RNASeqSampleMetaData metadata;
        }RNASeqSampleAlignment;

/*
      list of RNASeqSampleAlignment
*/

 typedef list<RNASeqSampleAlignment> RNASeqSampleAlignmentSet;


/*
  The workspace id for a Reference Annotation
  @id ws KBaseRNASeq.ReferenceAnnotation
*/

typedef string ws_reference_annotation_id;

/*
  The workspace id for a RNASeqSampleAlignment object
  @id ws KBaseRNASeq.RNASeqSampleAlignment
*/

typedef string ws_samplealignment_id

/*
    Object for RNASeq transcript assembly
    @metadata ws metadata.sample_id
    @metadata ws metadata.platform
    @metadata ws metadata.title
    @metadata ws metadata.source
    @metadata ws metadata.source_id
    @metadata ws metadata.sample_desc
    @metadata ws metadata.ref_genome

/*

  typedef structure{
        Handle handle1;
        RNASeqSampleMetaData metadata;
        }RNASeqCufflinkstranscriptAssembly;

/*
   list of RNASeqCufflinkstranscriptAssembly
*/

 typedef list<RNASeqCufflinkstranscriptAssemblySet>  RNASeqCufflinkstranscriptAssemblySet;

/*
    Object for RNASeq Merged transcriptome assembly
    @metadata ws metadata.sample_id
    @metadata ws metadata.platform
    @metadata ws metadata.title
    @metadata ws metadata.source
    @metadata ws metadata.source_id
    @metadata ws metadata.sample_desc
 @metadata ws metadata.ref_genome

/*

  typedef structure{
        Handle handle1;
        RNASeqSampleMetaData metadata;
        }RNASeqCuffmergetranscriptome;


/*
  The mapping object for the ws_rnaseqSample_id with the ws_samplealignment_id
*/

typedef mapping<ws_rnaseqSample_id sampleID,ws_samplealignment_id sampleAlignmentID> mapped_sample_alignment;

/*
  The mapping object for the ws_rnaseqSample_id with the ws_expression_sample_id
*/

typedef mapping<ws_rnaseqSample_id sampleID,expression_sample_id exp_sampleID> mapped_sample_expression;

/*
  Collection of the alignment files and transcript abundances for RNASeq experiment
  @optional expression_samples
*/

  typedef structure{
    string experiment_id;
    list<mapped_sample_alignment> alignment_files;
    list<mapped_sample_expression>  expression_samples;
    }RNASeqTuxedoResults;


/*
      RNASeqDifferentialExpression file structure
*/
  typedef structure {
      string name;
      Handle handle1;
  }RNASeqDifferentialExpressionFile;

/*
      list of RNASeqDifferentialExpression files
*/

  typedef list<RNASeqDifferentialExpressionFile> RNASeqDifferentialExpressionSet;


/*
    Object for the RNASeq Differential Expression
*/

 typedef structure {
     ExpressionSeries series_sample_expression_values;
RNASeqDifferentialExpressionSet diff_expression;
     }RNASeqCuffdiffDifferentialExpression;

/*

  Object to Describe the RNASeq experiment
  @optional title platform reference sample_short_names source tissue condition
*/

 typedef structure {
        string experiment_id
        string title;
        string platform;
        genome_id reference;
        int num_samples;
        int num_replicates;
        list<ws_rnaseqSample_id> sample_ids;
        list<string> sample_short_names;
        list<string> tissue;
        list<condition> condition;
        ws_reference_annotation annotation;
        string source;
        string Library_type;
        string publication_id;
        string source_id;
        string external_source_date;
        }RNASeqExperiment;

/* FUNCTIONS used in the service */

/* Function parameters to call tophat */

funcdef CallFastqc(fastqcParams params)
     return (string job_id) authentication required;

 typedef structure{
     ws_rnaseqSample_id sample_id;
     }fastqcParams;


funcdef TophatCall(TopHatParams params)
     return (string job_id) authentication required;

 typedef structure{
     ws_rnaseqSample_id sample_id;
     string output_obj_name;
     ws_reference_assembly_id reference;
     Tophat_opts opts_dict;
     ws_reference_annotation_id annotation_gtf;
     }TophatParams;

 typedef structure{
     string read-mismatches;
     string read-gap-length,;
     int read-edit-dist;
    int read-realign-edit-dist;
     bool bowtie1;
     string output-dir;
     int mate-inner-dist;
     int mate-std-dev;
     int min-anchor-length;
     int splice-mismatches;
     int min-intron-length;
     int max-intron-length;
     int max-insertion-length;
     int num-threads;
     int max-multihits;
     bool report-secondary-alignments;
     bool no-discordant;
     bool no-mixed;
     bool no-coverage-search;
     bool coverage-search;
     bool microexon-search;
     string library-type;
     int segment-mismatches;
     int segment-length;
     int min-segment-intron;
     int max-segment-intron;
     int min-coverage-intron;
     int max-coverage-intron;
     bool b2-very-fast;
     bool b2-fast;
     bool b2-sensitive;
     bool b2-very-sensitive;
     bool fusion-search;
     int fusion-anchor-length;
     int fusion-min-dist;
     int fusion-read-mismatches;
     int fusion-multireads;
     int fusion-multipairs;
     bool fusion-ignore-chromosomes;
     }Tophat_opts;


funcdef CufflinksCall(CufflinksParams params)
    return (string job_id) authentication required;

 typedef structure{
        ws_samplealignment_id alignment_sample_id;
        string output_obj_name;
 ws_reference_annotation_id annotation_gtf;
        Cufflinks_opts opts_dict;
        }CufflinksParams;


funcdef CuffmergeCall(CuffmergeParams params)
    return (string job_id) authentication required;

typedef structure{
        RNASeqTuxedoPipelineResults rnaseq_output_files;
        string output_obj_name;
        ws_reference_annotation_id annotation_gtf;
        Cuffmerge_opts opts_dict;
        }CuffmergeParams;


funcdef CuffdiffCall(CuffdiffParams params)
   return (string job_id) authentication required;

typedef structure{
        RNASeqTuxedoPipelineResults rnaseq_output_files;
        string output_obj_name;
        ws_reference_annotation_id annotation_gtf;
        Cuffdiff_opts opts_dict;
        }CuffdiffParams;

funcdef getAlignmentStats(AlignmentStatsParams params)
   return (string job_id) authentication required;

typedef structure{
        ws_samplealignment_id alignment_sample_id;
        }AlignmentStatsParams;

funcdef createExpressionHistogram(ExpressionHistogramParams params)
   return (string job_id) authentication required;

typedef structure{
        ws_expression_sample_id expression_sample;
        int number_of_bins;
        }ExpressionHistogramParams;


funcdef createExpressionSeries(ExpressionSeriesParams params)
   return (string job_id) authentication required;

typedef structure{
        RNASeqExperiment rnaseq_exp_details;
        ws_expression_sample_ids expression_sample_ids;
        }ExpressionSeriesParams;

funcdef createExpressionMatrix(ExpressionMatrix params)
   return (string job_id) authentication required;

typedef structure{
 RNASeqExperiment rnaseq_exp_details;
        RNASeqTuxedoResults rnaseq_results;
        }ExpressionMatrixParams;

};
