import string


class Template:
    def __init__(self, template_file : str) -> None:
        """ Parses a simple string.Template() file.
            Simple bash-like replacement of $placeholder happens.
        """
        with open(template_file) as fp:
            self.tmpl = string.Template(fp.read())

    def write(self, substitutions : dict, output_file : str):
        """ Write the substituted template to a file.
            Simple bash-like replacement of ${placeholder} happens.
            Raises KeyError if substitution does not contain a placeholder.
        """
        with open(output_file, 'w') as fp:
            fp.write(self.tmpl.substitute(substitutions))


class Error:
    @classmethod
    def report(cls, err : Exception, problem : str, *solutions):
        """ Reports a problem/exception. Provides solutions. """
        print("\n", str(problem).upper())
        for sol in solutions:
            print("\t" + sol)
        print()
        raise err

    @classmethod
    def check(cls, okcond : bool, problem : str, *solutions):
        """ Checks if a condition is True. Provides solutions. """
        if not okcond:
            print("\n", str(problem).upper())
            for sol in solutions:
                print("\t" + str(sol))
            print()
            raise RuntimeError(problem)

