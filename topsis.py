# topsis module
__author__ = '<j.fallon@pgr.reading.ac.uk>'
__version__ = 0.2

# Import for arrays, linalg, types
import numpy as np


class topsis:
    """ Define a TOPSIS decision making process
    TOPSIS (Technique for Order Preference by Similarity to an Ideal Solution)
    chooses and ranks alternatives of shortest distance from the ideal solution
    """
    C = None
    optimum_choice = None

    def __init__(self, a, w, I):
        """ Initialise topsis object with alternatives (a), weighting (w),
        and benefit/cost indicator (i). Validate the user input for correct
        dimensions etc.

        :param np.ndarray a: A 2D array of shape (J,n)
        :param np.ndarray w: A 1D array of shape (J)
        :param np.ndarray I: A 1D array of shape (n)
        """
        # Decision Matrix
        self.a = np.array(a).T
        assert len(self.a.shape) == 2, "Decision matrix a must be 2D"

        # Number of alternatives, aspects
        (self.n, self.J) = self.a.shape

        # Weight matrix
        self.w = np.array(w)
        assert len(self.w.shape) == 1, "Weights array must be 1D"
        assert self.w.size == self.n, "Weights array wrong length, " + \
                                      "should be of length {}".format(self.n)

        # Normalise weights to 1
        self.w = self.w/sum(self.w)

        # Benefit (True) or Cost (False) criteria?
        self.I = np.array(I)
        assert len(self.I.shape) == 1, "Criterion array must be 1D"
        assert len(self.I) == self.n, "Criterion array wrong length, " + \
                                      "should be of length {}".format(self.n)

        # Initialise best/worst alternatives lists
        ab, aw = np.zeros(self.n), np.zeros(self.n)
   
    
    def __repr__(self):
        """ What to print when the object is called?
        """
        # If optimum choice not yet calculated, start the calculation!
        if self.optimum_choice == None:
            self.calc()
        opt_idx = self.optimum_choice
        return 'Best alternative\na[{}]: {}'.format(opt_idx, self.a[:, opt_idx])
    
    
    def step1(self):
        """ TOPSIS Step 1
        Calculate the normalised decision matrix (self.r)
        """
        self.r = self.a/np.array(np.linalg.norm(self.a, axis=1)[:, np.newaxis])
        return
    
    
    def step2(self):
        """ TOPSIS Step 2
        Calculate the weighted normalised decision matrix
        Two transposes required so that indices are multiplied correctly:
        """
        self.v = (self.w * self.r.T).T
        return
    
    
    def step3(self):
        """ TOPSIS Step 3
        Determine the ideal and negative-ideal solutions
        I[i] defines i as a member of the benefit criteria (True) or the cost
        criteria (False)
        """
        # Calcualte ideal/negative ideals
        self.ab = np.max(self.v, axis=1) * self.I + \
                  np.min(self.v, axis=1) * (1 - self.I)
        self.aw = np.max(self.v, axis=1) * (1 - self.I) +  \
                  np.min(self.v, axis=1) * self.I
        return
   
    
    def step4(self):
        """ TOPSIS Step 4
        Calculate the separation measures, n-dimensional Euclidean distance
        """
        # Create two n long arrays containing Eculidean distances
        # Save the ideal and negative-ideal solutions
        self.db = np.linalg.norm(self.v - self.ab[:,np.newaxis], axis=0)
        self.dw = np.linalg.norm(self.v - self.aw[:,np.newaxis], axis=0)
        return
    

    def step5(self):
        """ TOPSIS Step 5 & 6
        Calculate the relative closeness to the ideal solution, then rank the
        preference order
        """
        # Ignore division by zero errors
        #np.seterr(all='ignore')
        # Find relative closeness
        self.C = self.dw / (self.dw + self.db)
        self.optimum_choice = self.C.argsort()[-1]
        return
   
    
    def calc(self):
        """ TOPSIS Calculations
        This can be called once the object is initialised, and is
        automatically called when a representation of topsis is
        needed (eg. print(topsis(matrix, weights, I)). This calls each step in
        TOPSIS algorithm and stores calcultions in self.

        The optimum alternatives index (starting at 0) is saved in
        self.optimum_choice
        """
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return

