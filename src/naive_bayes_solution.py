from bnetbase import Variable, Factor, BN
import csv
import itertools


def normalize(factor):
    '''
    Normalize the factor such that its values sum to 1.
    Do not modify the input factor.

    :param factor: a Factor object.
    :return: a new Factor object resulting from normalizing factor.
    '''

    ret_factor = Factor(f"Normalized:{factor.name}", factor.get_scope())
    total = sum(factor.values)
    for value in range(len(ret_factor.values)):
        ret_factor.values[value] = factor.values[value] / total
        # print(factor.values[value])
    return ret_factor


def restrict(factor, variable, value):
    '''
    Restrict a factor by assigning value to variable.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to restrict.
    :param value: the value to restrict the variable to
    :return: a new Factor object resulting from restricting variable to value.
             This new factor no longer has variable in it.

    '''
    # Used the aid of CHatGPT for the inner for loop logic; helped repair mine
    variable.set_assignment(value)
    scope2 = factor.get_scope()
    scope2.remove(variable)
    ret_factor = Factor(
        f"Restrict:{factor.name}; {variable.name}={value}", scope2)

    for i in range(len(ret_factor.values)):
        temp = i
        for var in reversed(scope2):  #ChatGPT used for this (inner) loop logic
            var.set_assignment_index(temp % var.domain_size())
            temp = temp // var.domain_size()

        ret_factor.values[i] = factor.get_value_at_current_assignments()

    return ret_factor

    # raise NotImplementedError


def sum_out(factor, variable):
    '''
    Sum out a variable variable from factor factor.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to sum out.
    :return: a new Factor object resulting from summing out variable from the factor.
             This new factor no longer has variable in it.
    '''

    scope2 = factor.get_scope()
    scope2.remove(variable)
    ret_factor = Factor(f"Sum-Out:{factor.name};{variable.name}",
                        scope2)

    for i in range(len(ret_factor.values)):
        # variable.set_assignment_index(0)
        temp = i
        ret_factor.values[i] = 0
        for var in reversed(scope2): # Reused logic from restrict()
            var.set_assignment_index(temp % var.domain_size())
            temp = temp // var.domain_size()
        for ind in range(len(variable.domain())):
            variable.set_assignment_index(ind)
            ret_factor.values[i] += factor.get_value_at_current_assignments()

    # ret_factor.values[i] = factor.get_value_at_current_assignments()
    # variable.set_assignment_index(1)
    # ret_factor.values[i] += factor.get_value_at_current_assignments()

    return ret_factor
    # raise NotImplementedError


def return_smallest_scope(factor_list):
    return min(factor_list, key=lambda factor: len(factor.scope))


def return_index_factor(factor_list, factor):
    # print(factor.name)
    for i in range(len(factor_list)):
        if factor_list[i].name == factor.name:
            return i
    return None


def find_scope_within(factor_list: list[Factor], scope):
    for i in factor_list:
        check = True
        for a in scope:
            if a not in i.scope:
                check = False
        if check:
            return i
        # l = 0
        # for b in i.scope:
        #     if b in scope:
        #         l+= 1
        # if l == len(scope):
        #     return i
    return None


def multiply_logic(f1: Factor, f2: Factor):

    # new_scope = f1.get_scope() + [v for v in f2.get_scope() if
    #                               v not in f1.get_scope()]
    new_scope = f2.get_scope() + [v for v in f1.get_scope() if
                                  v not in f2.get_scope()]
    ret_factor = Factor(f"Multiplied:{f1.name} and {f2.name}", new_scope)

    for i in range(len(ret_factor.values)):
        temp = i
        # asgn = {}
        for var in new_scope:
            new_index = temp % var.domain_size()
            var.set_assignment_index(new_index)
            temp = temp//var.domain_size()
        # for var in f1.get_scope():
        #     var.set_assignment(asgn[var])
        # for var in f2.get_scope():
        #     var.set_assignment(asgn[var])

        ret_factor.add_value_at_current_assignment(
            f1.get_value_at_current_assignments() *
            f2.get_value_at_current_assignments())

    return ret_factor


def multiply(factor_list):
    '''
    Multiply a list of factors together.
    Do not modify any of the input factors.

    :param factor_list: a list of Factor objects.
    :return: a new Factor object resulting from multiplying all the factors in factor_list.
    '''
    # checked = []
    while len(factor_list) > 1:

        f1 = factor_list.pop()
        f2 = factor_list.pop()
        f3 = multiply_logic(f1, f2)
        factor_list.append(f3)
        # factor_list.insert(0, f3)
        # f3.print_table()
        # print("")
        # f1_index = return_index_factor(factor_list,
        #                                return_smallest_scope(factor_list))
        # f1 = factor_list.pop(f1_index)
        # pot_f2 = find_scope_within(factor_list, f1.scope)
        # f2_index = return_index_factor(factor_list, pot_f2)
        # f2 = factor_list.pop(f2_index)
        # print(f1.name, f2.name)
        # f3 = multiply_logic(f1, f2)
        # factor_list.append(f3)
    # f4 = factor_list.pop()
    # f4.print_table()
    # print("")
    return factor_list.pop()
    # raise NotImplementedError


def ve(bayes_net, var_query, EvidenceVars):
    '''
    Execute the variable elimination algorithm on the Bayesian network to compute
    a distribution over the values of var_query given the evidence provided by EvidenceVars.

    :param bayes_net: a BN object.
    :param var_query: the query variable.
    :param EvidenceVars: the evidence variables.
    :return: A normalized Factor object representing the query variable's distribution.
    '''
    factor_list = bayes_net.factors()
    # print(factor_list)
    # print(bayes_net.get_variable("Salary").get_assignment())
    for ev in EvidenceVars:
        # print(ev.name)
        for i in range(len(factor_list)):
            # print("")
            if ev in factor_list[i].get_scope():
                factor_list[i] = restrict(factor_list[i], ev, ev.get_evidence())

    for var in bayes_net.variables():
        if var != var_query and var not in EvidenceVars:
            filtered = []
            new_fact_lst = []
            for fact in factor_list:
                if var in fact.get_scope():
                    filtered.append(fact)
                else:
                    new_fact_lst.append(fact)
            factor_list = new_fact_lst
            # print(filtered)
            # print(factor_list)
            # print("---------------")
            if filtered != []:
                combined_factor = multiply(filtered)
                # combined_factor.print_table()
                # print("")
                reduced_factor = sum_out(combined_factor, var)
                # reduced_factor.print_table()
                factor_list.append(reduced_factor)

    result_factor = multiply(factor_list)
    # result_factor.print_table()
    # print("")
    # raise NotImplementedError
    return normalize(result_factor)


def naive_bayes_model(data_file, variable_domains={
    "Work": ['Not Working', 'Government', 'Private', 'Self-emp'],
    "Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional',
                  'Bachelors', 'Masters', 'Doctorate'],
    "Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour',
                   'Service', 'Professional'],
    "MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'],
    "Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family',
                     'Other-relative', 'Unmarried'],
    "Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo',
             'Other'], "Gender": ['Male', 'Female'],
    "Country": ['North-America', 'South-America', 'Europe', 'Asia',
                'Middle-East', 'Carribean'], "Salary": ['<50K', '>=50K']},
                      class_var=Variable("Salary", ['<50K', '>=50K'])):
    '''
   NaiveBayesModel returns a BN that is a Naive Bayes model that
   represents the joint distribution of value assignments to
   variables in the Adult Dataset from UCI.  Remember a Naive Bayes model
   assumes P(X1, X2,.... XN, Class) can be represented as
   P(X1|Class)*P(X2|Class)* .... *P(XN|Class)*P(Class).
   When you generated your Bayes bayes_net, assume that the values
   in the SALARY column of the dataset are the CLASS that we want to predict.
   @return a BN that is a Naive Bayes model and which represents the Adult Dataset.
    '''
    ### READ IN THE DATA
    input_data = []
    with open(data_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  #skip header row
        for row in reader:
            input_data.append(row)

    # print(input_data[0])
    # print()
    # print(input_data[1])
    # print(headers.index("Salary"))

    ### DOMAIN INFORMATION REFLECTS ORDER OF COLUMNS IN THE DATA SET
    #variable_domains = {
    #"Work": ['Not Working', 'Government', 'Private', 'Self-emp'],
    #"Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional', 'Bachelors', 'Masters', 'Doctorate'],
    #"Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour', 'Service', 'Professional'],
    #"MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'],
    #"Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
    #"Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'],
    #"Gender": ['Male', 'Female'],
    #"Country": ['North-America', 'South-America', 'Europe', 'Asia', 'Middle-East', 'Carribean'],
    #"Salary": ['<50K', '>=50K']
    #}

    factor_lst = []

    class_fact = Factor(f"P({class_var.name})", [class_var])
    total_freq = 0
    class_freq = {}
    for a in class_var.domain():
        class_freq[a] = 0

    var_dict = {}
    var_list = []
    for a, b in variable_domains.items():
        # var_dict[a] = Variable(a, b)
        if a != class_var.name:
            variable = Variable(a, b)
            var_dict[a] = variable
            var_list.append(variable)
        else:
            var_dict[a] = class_var
            var_list.append(class_var)

    # Got help from chatGPT for counting logic;
    # including using a dict of tuples to keep track of frequency.
    for row in input_data:
        class_freq[row[headers.index(class_var.name)]] += 1
        total_freq += 1

    for i in class_freq.keys():
        class_fact.add_values([[i, (class_freq[i] / total_freq)]])

    factor_lst.append(class_fact)

    for name, variable in var_dict.items():
        new_fact_freq = {}
        if name != class_var.name:
            new_fact = Factor(f"P({name}|{class_var.name})",
                              [variable, class_var])
            for val in variable.domain():
                for val2 in class_var.domain():
                    new_fact_freq[(val, val2)] = 0

            for row in input_data:
                new_fact_freq[(row[headers.index(name)],
                               row[headers.index(class_var.name)])] += 1

            for val2 in class_var.domain():
                class_sum = 0
                for val in variable.domain():
                    class_sum += new_fact_freq[val, val2]
                for val in variable.domain():
                    if class_sum > 0:
                        cond_prob = new_fact_freq[val, val2] / class_sum
                    else:
                        cond_prob = 0
                    new_fact.add_values([[val, val2, cond_prob]])
            factor_lst.append(new_fact)
    # print("")
    # print(var_dict.values())
    # [print(f.scope) for f in factor_lst]
    # print(var_dict.values())
    # print("---------------------")
    return BN("NaiveBayesModel", var_list, factor_lst)
    # raise NotImplementedError


def get_prob(query, evidence, bayes: BN, value):

    # for a, b in evidence.items():
    #     bayes.get_variable(a).set_evidence(b)
    #
    # ev = []
    # for a in evidence.keys():
    #     ev.append(bayes.get_variable(a))
    # ret = ve(bayes, query, ev)
    # print("")

    ret = ve(bayes, query, evidence)

    return ret.get_value([value])


def explore(bayes_net, question):
    '''    Input: bayes_net---a BN object (a Bayes bayes_net)
           question---an integer indicating the question in HW4 to be calculated. Options are:
           1. What percentage of the women in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
           2. What percentage of the men in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
           3. What percentage of the women in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
           4. What percentage of the men in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
           5. What percentage of the women in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
           6. What percentage of the men in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
           @return a percentage (between 0 and 100)
    '''

    # Read test data
    input_data = []
    with open('data/adult-test.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # Skip header row
        for row in reader:
            input_data.append(row)

    E1 = ["Work", "Occupation", "Education", "Relationship"]
    E2 = ["Work", "Occupation", "Education", "Relationship", "Gender"]

    salary = bayes_net.get_variable("Salary")

    asgn = []
    for row in input_data:
        ev1, ev2 = {}, {}
        for var in E1:
            ev1[var] = row[headers.index(var)]
        for var in E2:
            ev2[var] = row[headers.index(var)]

        ev1_asgn, ev2_asgn = [], []
        for var in E1:
            ev1_asgn.append(bayes_net.get_variable(var))
        for var in E2:
            ev2_asgn.append(bayes_net.get_variable(var))

        for var in ev1_asgn:
            var.set_evidence(ev1[var.name])
        pr1 = ve(bayes_net, salary, ev1_asgn).get_value([">=50K"])

        for var in ev2_asgn:
            var.set_evidence(ev2[var.name])
        pr2 = ve(bayes_net, salary, ev2_asgn).get_value([">=50K"])
        # print(pr1, pr2)

        # if pr1 > pr2:
        #     print("hi")

        asgn.append({"G": row[headers.index("Gender")], "RS":
            row[headers.index("Salary")], "pr1": pr1, "pr2": pr2})

    total = 0
    conditional = 0
    gender_check = ""

    if question == 1 or question == 2:
        if question == 1:
            gender_check = "Female"
        else:
            gender_check = "Male"
        for a in asgn:
            if a["G"] == gender_check and a["pr1"] > a["pr2"]:
                conditional += 1
            if a["G"] == gender_check:
                total += 1
    elif question == 3 or question == 4:
        if question == 3:
            gender_check = "Female"
        else:
            gender_check = "Male"
        for a in asgn:
            if (a["G"] == gender_check and a["RS"] == ">=50K" and a["pr1"] >
                    0.5):
                conditional += 1
            if a["G"] == gender_check and a["pr1"] > 0.5:
                total += 1
    elif question == 5 or question == 6:
        if question == 5:
            gender_check = "Female"
        else:
            gender_check = "Male"
        for a in asgn:
            if a["G"] == gender_check and a["pr1"] > 0.5:
                conditional += 1
            if a["G"] == gender_check:
                total += 1
    # print(total)
    if total == 0:
        return 0
    return (conditional / total) * 100
    # return 0
    # raise NotImplementedError


if __name__ == '__main__':
    nb = naive_bayes_model('data/adult-train.csv')
    for i in range(1, 7):
        print("explore(nb,{}) = {}".format(i, explore(nb, i)))
    # print(explore(nb, 5))
