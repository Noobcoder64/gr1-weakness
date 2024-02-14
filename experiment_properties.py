import io_utils as io
import timeit
import random
from datetime import datetime

# Set random seed for repeatability
random.seed(datetime.now())


case_study_name = "SYNTECH15-UNREAL-1/PcarLTL_394_PCar.spectra_1"
generation_method = "multivarbias"
n_multivarbias = 5
goodness_measure = ""
goodness_update_required = False
search_method = "minimal-bfs"
refinement_method = generation_method + ("-" + search_method if search_method != "" else "") + ("-" + goodness_measure if goodness_measure != "" else "")
exp_number = "bfs_minimal_hybrid"
limit_fairness = -1 # Max fairness conditions allowed in the experiment. -1 if unlimited
include_parent_unreal_core_check = True


# Decide whether the search should return initial conditions, invariants, and/or fairness conditions
# By default, they are all True
search_initials = True
search_invariants = True
search_fairness = True

# In case a subfolder of DataFiles is used for the data, must include "/" character afterwards
subfolder = "DataThesis/BFS_Minimal_Hybrid/Hybrid/"

# This is a reference to the original specification file
specfile = "Examples/"+case_study_name+".rat"
datafile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+".csv"
checkpointfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_checkpoint.csv"
satfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_sat.csv"
weaknessfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_weakness.csv"
wellsepfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_wellsep.csv"
statsfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_stats.csv"
equivclassesfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_equivclasses.csv"
distancesfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_distances.csv"
cstimesfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_cstimes.csv"
uniquesolsfile = "DataFiles/"+ subfolder + case_study_name + "_"+refinement_method+"_exp"+str(exp_number)+"_uniquesols.csv"

experimentstatsfile = "DataFiles/" + subfolder + case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_expstats.csv"

inputVarsList = io.extractInputVariablesFromFile(specfile)
outputVarsList = io.extractOutputVariablesFromFile(specfile)
varsList = inputVarsList + outputVarsList
initialGR1Units = io.extractAssumptionList(specfile)
guaranteesList = io.extractGuaranteesList(specfile)

counterstrategies = [] # This list contains all observed counterstrategy bdds for use in the experiment
                       # Each element is a triple (marduk_instance, bdd_initial_states, bdd_transition)

start_experiment = timeit.default_timer()

def changeCaseStudy(case_study_name):
    global specfile
    global datafile
    global checkpointfile
    global satfile
    global weaknessfile
    global wellsepfile
    global statsfile
    global equivclassesfile
    global distancesfile
    global cstimesfile

    global experimentstatsfile

    global inputVarsList
    global outputVarsList
    global varsList
    global initialGR1Units
    global guaranteesList

    global start_experiment

    if case_study_name.endswith(".rat"):
        case_study_name = case_study_name[:-4]

    specfile = "Examples/" + case_study_name + ".rat"
    datafile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + ".csv"
    checkpointfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_checkpoint.csv"
    satfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_sat.csv"
    weaknessfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_weakness.csv"
    wellsepfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_wellsep.csv"
    statsfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_stats.csv"
    equivclassesfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(
        exp_number) + "_equivclasses.csv"
    distancesfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(
        exp_number) + "_distances.csv"
    cstimesfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_cstimes.csv"
    uniquesolsfile = "DataFiles/" + subfolder + case_study_name + "_"+refinement_method+"_exp"+str(exp_number)+"_uniquesols.csv"

    experimentstatsfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_expstats.csv"

    inputVarsList = io.extractInputVariablesFromFile(specfile)
    outputVarsList = io.extractOutputVariablesFromFile(specfile)
    varsList = inputVarsList + outputVarsList
    initialGR1Units = io.extractAssumptionList(specfile)
    guaranteesList = io.extractGuaranteesList(specfile)

    start_experiment = timeit.default_timer()

def changeGenerationMethod(generation_method):
    global specfile
    global datafile
    global checkpointfile
    global satfile
    global weaknessfile
    global wellsepfile
    global statsfile
    global equivclassesfile
    global distancesfile
    global cstimesfile

    global experimentstatsfile

    global inputVarsList
    global outputVarsList
    global varsList
    global initialGR1Units
    global guaranteesList

    global start_experiment

    refinement_method = generation_method + ("-" + search_method if search_method != "" else "") + (
    "-" + goodness_measure if goodness_measure != "" else "")

    specfile = "Examples/" + case_study_name + ".rat"
    datafile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + ".csv"
    checkpointfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_checkpoint.csv"
    satfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_sat.csv"
    weaknessfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_weakness.csv"
    wellsepfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_wellsep.csv"
    statsfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(exp_number) + "_stats.csv"
    equivclassesfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(
        exp_number) + "_equivclasses.csv"
    distancesfile = "DataFiles/" + subfolder + case_study_name + "_" + refinement_method + "_exp" + str(
        exp_number) + "_distances.csv"
    cstimesfile = "DataFiles/"+ subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_cstimes.csv"
    uniquesolsfile = "DataFiles/" + subfolder + case_study_name + "_"+refinement_method+"_exp"+str(exp_number)+"_uniquesols.csv"

    experimentstatsfile = "DataFiles/"+subfolder+case_study_name+"_"+refinement_method+"_exp"+str(exp_number)+"_expstats.csv"

    inputVarsList = io.extractInputVariablesFromFile(specfile)
    outputVarsList = io.extractOutputVariablesFromFile(specfile)
    varsList = inputVarsList + outputVarsList
    initialGR1Units = io.extractAssumptionList(specfile)
    guaranteesList = io.extractGuaranteesList(specfile)

    start_experiment = timeit.default_timer()

def getCaseStudyAndGenerationMethodFromFilename(filename):
    # If there is a path in the filename, isolate the file name
    filename = filename.split("/")[-1]
    if "_interpolation-" in filename or "_interpolation_" in filename:
        case_study = filename[:filename.index("_interpolation-")]
        generation_method = "interpolation"
    elif "_multivarbias-" in filename or "_multivarbias_" in filename:
        case_study = filename[:filename.index("_multivarbias-")]
        generation_method = "multivarbias"

    return (case_study, generation_method)
