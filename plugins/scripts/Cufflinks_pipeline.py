#!/usr/bin/python
"""
####################
Cufflinks_pipeline.py
####################
Code defining an object oriented python pipeline script to allow simplified
coordination of data through parts or all of the popular Cufflinks
RNA-seq analysis suite.
"""


import sys
import argparse
import re

import yaml
import json
try:
    import pprocess
except ImportError:
    pprocess = False
    pass

from bunch import bunchify
from externals import *
from errors import *
from call_utils import *
from misc import *

def start_prog(args_prog, test_vals):
    """
    Manage testing whether a program block should be entered based on the contents of args.prog.

    :param args_prog: `list` of program names.
    :param test_vals: `list` of strings that should trigger returning `True`
    :return: `bool`
    """
    return any((prog in test_vals) for prog in args_prog)

def main():
    """
    The main loop.  Lets ROCK!
    """

    desc = """This script reads options from a yaml formatted file and organizes the execution of tophat/cufflinks
    runs for multiple condition sets."""

    parser = argparse.ArgumentParser(description=desc)

    #parser.add_argument('--version', action='version', version='%(prog)s ' + blacktie.__version__,
    #               	help="""Print version number.""")    
    parser.add_argument('--config_file', type=str,
                        help="""Path to a yaml formatted config file containing setup options for the runs.""")
    parser.add_argument('--prog', type=str, nargs='+', choices=['tophat', 'cufflinks', 'cuffmerge', 'cuffdiff',
                                                                'cummerbund', 'all'], default='tophat',
                        help="""Which program do you want to run? (default: %(default)s)""")
    parser.add_argument('--hide-logs', action='store_true', default=False,
                        help="""Make your log directories hidden to keep a tidy 'looking' base directory. (default:
                        %(default)s)""")
    parser.add_argument('--mode', type=str, choices=['analyze', 'dry_run', 'qsub_script'], default='analyze',
                        help="""1) 'analyze': run the analysis pipeline. 2) 'dry_run': walk through all steps that
                        would be run and print out the command lines; however, do not send the commands to the
                        system to be run. 3) 'qsub_script': generate bash scripts suitable to be sent to a compute
                        cluster's
                        SGE through the qsub command. (default: %(default)s)""")    

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    args = parser.parse_args()

    yargs = bunchify(yaml.load(open(args.config_file, 'rU')))
    print 'yargs is ' + json.dumps(yargs)
    # set up run_id, log files, and email info
    if yargs.run_options.run_id:
        run_id = yargs.run_options.run_id
    else:

        run_id = get_time()

    base_dir = yargs.run_options.base_dir.rstrip('/')
    if args.hide_logs:
        run_logs = '%s/.%s.logs' % (base_dir, run_id)
    else:
        run_logs = '%s/%s.logs' % (base_dir, run_id)

    if not args.mode == 'dry_run':
        mkdirp(run_logs)
    else:
        pass

    yaml_out = '%s/%s.yaml' % (run_logs, run_id)

    # copy yaml config file with run_id as name for records
    if not args.mode == 'dry_run':
        shutil.copyfile(args.config_file, yaml_out)
    else:
        pass

    yargs.prgbar_regex = re.compile('>.+Processing.+\[.+\].+%\w*$')
    print 'length is ' + str(len(yargs.condition_queue))
    if len(yargs.condition_queue) > 1:
	print 'inside the if conditions'
    	yargs.groups = map_condition_groups(yargs)
    else:
	print 'inside the else contiions'
	yargs.groups = yargs.condition_queue[0]
    yargs.call_records = {}

    print ' yargs groups is ' + json.dumps(yargs.groups)
    # loop through the queued conditions and send reports for tophat

    if start_prog(args.prog, ['cufflinks', 'all']):
        # attempt to run more than one cufflinks call in parallel since cufflinks
        # seems to use only one processor no matter the value of -p you give it and
        # doesn't seem to consume massive amounts of memory 
        print "[Note] Starting cufflinks step.\n"
        try:
            if args.mode == 'dry_run':
                raise errors.BlacktieError("dry run")
            
            #  TODO: on mac pprocess raised AttributeError "module" has no attrb "poll" or some crap
            try:
                queue = pprocess.Queue(limit=yargs.cufflinks_options.p)
            except AttributeError as exc:
                if 'poll' in str(exc):
                    raise(errors.BlacktieError('no poll'))
                else:
                     raise

            def run_cufflinks_call(cufflinks_call):
                """
                function to start each parallel cufflinks_call inside the parallel job server.
                """
                cufflinks_call.execute()
                return cufflinks_call

            def change_processor_count(cufflinks_call):
                """
                Since we will run multiple instances of CufflinksCall at once, reduce
                the number of processors any one system call thinks it can use.
                """
                cufflinks_call.opt_dict['p'] = 2
                cufflinks_call.construct_options_list()
                cufflinks_call.options_list.extend([cufflinks_call.accepted_hits])
                cufflinks_call.arg_str = ' '.join(cufflinks_call.options_list)
                return cufflinks_call

            execute = queue.manage(pprocess.MakeParallel(run_cufflinks_call))
            jobs = []
            for condition in yargs.condition_queue:
                cufflinks_call = CufflinksCall(yargs, run_id, run_logs, conditions=condition,
                                               mode=args.mode)
                cufflinks_call = change_processor_count(cufflinks_call)
                jobs.append(cufflinks_call)
                execute(cufflinks_call)

            # record the cufflinks_call objects
            for call in queue:
                yargs.call_records[call.call_id] = call

        except (NameError, errors.BlacktieError) as exc:

            if ("'pprocess' is not defined" in str(exc)) or (str(exc) == "dry run") or (str(exc) == 'no poll'):
                pass
            else:
                raise
            
            print "Running cufflinks in serial NOT parallel.\n"
            # loop through the queued conditions and send reports for cufflinks    
            for condition in yargs.condition_queue:   
                # Prep cufflinks_call
                cufflinks_call = CufflinksCall(yargs,run_id, run_logs, conditions=condition,
                                               mode=args.mode)
                cufflinks_call.execute()

                # record the cufflinks_call object
                yargs.call_records[cufflinks_call.call_id] = cufflinks_call
    else:
        print "[Note] Skipping cufflinks step.\n"

if __name__ == "__main__":
    main()
