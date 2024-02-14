import re
import specification as sp

# Returns a list with all assumptions in a spec
def extractAssumptionList(spec):
    spec = [re.sub(r"\s", "", spec[i + 1]) for i, line in enumerate(spec) if re.search("asm|assumption", line)]
    return spec

# Returns a list with all guarantees in a .
def extractGuaranteesList(spec):
    spec = [re.sub(r"\s", "", spec[i + 1]) for i, line in enumerate(spec) if re.search("gar|guarantee", line)]
    return spec

# Extract input variables from a specification
def extractInputVariables(spec):
    variables = []
    for line in spec:
        match = re.search(r'(?:env)\s+boolean\s+(\w+)\s*', line)
        if match:
            variables.append(match.group(1))
    return variables

# Extract output variables from a specification
def extractOutputVariables(spec):
    variables = []
    for line in spec:
        match = re.search(r'(?:sys|aux)\s+boolean\s+(\w+)\s*', line)
        if match:
            variables.append(match.group(1))
    return variables

# Extract variables as a list from a string formula
def extractVariablesFromFormula(phi):
    exclude = {"G", "F", "GF", "X", "next", "U", "true", "false", "and"}
    return [x for x in re.findall("\w+", phi) if x not in exclude]


# varpattern matches variable names in LTL formulae
varpattern = re.compile(r"\b(?!TRUE|FALSE)\w+")

def getDistinctVariablesInFormula(formula):
    """Returns the set of all distinct variables appearing in formula"""
    varset = set(varpattern.findall(formula))
    varset.discard("X")
    varset.discard("G")
    varset.discard("F")
    return varset


def main():
    spec = sp.read_file("Lift.spectra")
    spec = sp.interpolation_spec(spec)

    inputVars = extractInputVariables(spec)
    outputVars = extractOutputVariables(spec)
    assumptions = extractAssumptionList(spec)
    guarantees = extractGuaranteesList(spec)

    print("=== INPUT VARS ===")
    print('\n'.join(inputVars))
    print("=== OUTPUT VARS ===")
    print('\n'.join(outputVars))
    print("=== ASSUMPTIONS ===")
    print('\n'.join(assumptions))
    print("=== GUARANTEES ===")
    print('\n'.join(guarantees))


if __name__=="__main__":
    main()