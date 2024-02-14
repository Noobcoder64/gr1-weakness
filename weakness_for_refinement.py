import experiment_properties as exp
import automaton as a
import syntax_utils as su
import nondeterministic_tgba as ndtgba
import numpy as np
from io_utils import extractVariablesFromFormula

# This module computes the weakness measure in another way suitable for assumptions refinement.
# d1 is the same as normal weakness: Hausdorff dimension of the entire formula.
# The only difference is that the function here only requires the refinement part as input, so as
# to make the interface consistent with d2.
# d2 measures how many suffixes are cut out from

def computeWeakness_probe(phi, var_set):
    """Computes the weakness measure of a GR(1) refinement phi.
    This is the Hausdorff dimension of the language removed from the initial assumptions by the additional fairness
    conditions in the refinement.
    Adds some probes for evaluation purposes"""

    # Probes. We only account for the initial automaton and the intersection ones. The cfair ones and the subGraph ones
    # require shorter time than those and do not report them
    num_automata = 0 # Includes the initial automaton and all the intersection automata.
    times_automata = [] # Reports the time to compute each automaton.
    numstates_automata = [] # Reports the number of states of each automaton


    # First get the base of the difference: accepting strongly connected components of the original automaton
    ltlFormula = " & ".join(exp.initialGR1Units)
    if ltlFormula == "":
        ltlFormula = phi
    elif phi != "":
        ltlFormula = ltlFormula + " & " + phi
    automaton = a.Automaton("ltl", ltlFormula=ltlFormula, var_set=var_set)
    #automaton = a.Automaton("ltl", ltlFormula=phi, var_set=var_set)
    d1 = automaton.getEntropy()
    d2 = automaton.getHausdorffDimension()
    num_automata += 1
    times_automata.append(automaton.automaton_compute_time)
    numstates_automata.append(automaton.numstates)

    # WORKAROUND to eliminate initial conditions from initial assumptions
    init_assumptions = " & ".join([x for x in exp.initialGR1Units if x.startswith("G(")])

    num_max_entropy_sccs = len(automaton.sccs_maxentropy)

    su.parserInit()
#    initials = su.parseInitials(phi)
#    invariants = su.parseInvariants(phi)
    cfairness = su.getCFairness(phi)

    if cfairness != []:
        # In order to get the second component of the measure
        #  - extract the maximum-entropy accepting SCCs of the language
        #  - combine them with the negation of every fairness condition
        #  - take the Hausdorff dimension of the suffixes deleted from every SCC by every fairness condition
        #  - the maximum of those is the Hausdorff dimension of the suffixes deleted from the maximum-entropy accepting SCCs
        sccs_maxentropy = automaton.sccs_maxentropy
        sccs_automata = []
        # This puts the maximum entropy automata into sccs_automata
        for scc in sccs_maxentropy:
            scc_closure = automaton.getSubgraph(scc)
            scc_closure.turnIntoClosure()
            sccs_automata.append(scc_closure)

        # This computes the automata of the negation of every fairness condition (or better, with the accepting part
        # of these automata).
        # In every case this is just one self-looping state with the loop's label being the boolean expression cfair = \lnot fair
        cfairness_automata = []
        for cfair in cfairness:
            cfairness_automata.append(a.Automaton("ltl",ltlFormula="G("+cfair+")",var_set=var_set))

        max_entropy_deleted_language = -np.inf
        for scc_automaton in sccs_automata:
            for cfair_automaton in cfairness_automata:
                # This has the effect of adding the conjunct cfair to every edge in scc_automaton, thus reducing the multiplicity
                # of these edges by the number of valuations that violate cfair
                removed_suffixes_component = a.IntersectionAutomaton(scc_automaton, cfair_automaton)
                num_automata += 1
                numstates_automata.append(removed_suffixes_component.numstates)
                times_automata.append(removed_suffixes_component.automaton_compute_time)

                entropy = removed_suffixes_component.getHausdorffDimension()
                if entropy > max_entropy_deleted_language:
                    max_entropy_deleted_language = entropy

    else:
        max_entropy_deleted_language = -np.inf

    weakness = Weakness(d1, d2, num_max_entropy_sccs, max_entropy_deleted_language)

    return (weakness, num_automata, numstates_automata, times_automata, automaton.is_strongly_connected)

class Weakness:
    """This class is used to define the correct ordering of the weakness measure"""

    def __init__(self, d1, d2, nummaxentropysccs, d3):
        self.d1 = d1 or -np.inf
        self.d2 = d2
        self.nummaxentropysccs = nummaxentropysccs
        self.d3 = d3

    def __lt__(self, other):
        # isclose used instead of == to deal with numeric approximation
        if not np.isclose(self.d1, other.d1, 1e-9, 1e-9):
            return self.d1 < other.d1
        elif not np.isclose(self.d2, other.d2, 1e-9, 1e-9):
            return self.d2 < other.d2
        else:
            return self.nummaxentropysccs < other.nummaxentropysccs \
                    or (self.nummaxentropysccs == other.nummaxentropysccs and self.d3 > other.d3)


    def __gt__(self, other):
        # isclose used instead of == to deal with numeric approximation
        if not np.isclose(self.d1, other.d1, 1e-9, 1e-9):
            return self.d1 > other.d1
        elif not np.isclose(self.d2, other.d2, 1e-9, 1e-9):
            return self.d2 > other.d2
        else:
            return self.nummaxentropysccs > other.nummaxentropysccs \
                    or (self.nummaxentropysccs == other.nummaxentropysccs and self.d3 < other.d3)


    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        return (self >= other) and (self <= other)

    def __str__(self):
        return str((self.d1, self.d2, self.nummaxentropysccs, self.d3))

    def __repr__(self):
        return str((self.d1, self.d2, self.nummaxentropysccs, self.d3))

def compareViaImplication(phi1,phi2,var_set=None):
    """Returns 0 if phi1 and phi2 do not imply each other, 1 if phi1 -> phi2, -1 if phi2 -> phi1, and 2 if phi1 and phi2
    are equivalent"""
    # # If the Hausdorff dimension of phi1 & !phi2 is -infty, then the automaton is empty, so !phi1 | phi2 must be valid,
    # # that is phi1 -> phi2 is valid
    # hausdim_phi1_not_phi2 = computeD1(phi1 + " & !(" + phi2 + ")",var_set)
    # hausdim_phi2_not_phi1 = computeD1(phi2 + " & !(" + phi1 + ")",var_set)
    #
    # if hausdim_phi1_not_phi2 == -np.inf and hausdim_phi2_not_phi1 == -np.inf:
    #     return 2
    # # Symmetric case when phi2 -> phi1
    # elif hausdim_phi2_not_phi1 == -np.inf:
    #     return -1
    # elif hausdim_phi1_not_phi2 == -np.inf:
    #     return 1
    # else:
    #     return 0
    if var_set is None:
        var_set = extractVariablesFromFormula(phi1 + " & " + phi2)

    tgba_phi1_not_phi2 = ndtgba.NondeterministcTGBA('ltl', ltlFormula=phi1 + " & !(" + phi2 + ")", var_set=var_set)
    tgba_phi2_not_phi1 = ndtgba.NondeterministcTGBA('ltl', ltlFormula=phi2 + " & !(" + phi1 + ")",
                                                    var_set=var_set)
    empty_phi1_not_phi2 = tgba_phi1_not_phi2.checkEmptiness()
    empty_phi2_not_phi1 = tgba_phi2_not_phi1.checkEmptiness()
    if empty_phi1_not_phi2 and empty_phi2_not_phi1:
        return 2
    elif empty_phi2_not_phi1:
        return -1
    elif empty_phi1_not_phi2:
        return 1
    else:
        return 0

def main():
#    print compareViaImplication("G((a&b) -> Xc) & a", "G((a&b) -> Xc) & G(F(a&b&c))", ['a', 'b', 'c'])
#    print compareViaImplication("G((a) -> Xc) & G(F(a&b&c&d))", "G(F(a&b&d))",  ['a', 'b', 'c'])

#    print str(computeWeakness_probe("G(a -> Xc)", ['a','b','c','d']))
#    print str(computeWeakness_probe("G((a) -> Xc) & G(F(a&b&c&d))", ['a','b','c','d']))

#    print str(computeWeakness_probe(" & ".join([u'G(F( (!hbusreq0) ))', '!(!hready)']), exp.varsList))
#    print Weakness(0.6000000000000001, 0.6000000000000001, 1, 0.5) > Weakness(0.6, 0.6, 2, 0.5)
    print str(computeWeakness_probe(" & ".join(['G((isReady & !frontDistSense_0) -> X(!(!frontDistSense_0 & isReady)))', 'G(F(!(!balancer_2) & !(balancer_1) & !(balancer_0)))']), exp.varsList))


if (__name__=='__main__'):
    main()
