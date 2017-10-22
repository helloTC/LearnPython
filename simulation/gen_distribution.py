import random
import math

class GenDistribution(object):
    """
    A class to generate variates that satisfied specific distribution
    """
    def __init__(self):
        """
        """
        pass

    def uniform(self, a, b):
        """
        Generate random number that satisfied to uniform distribution

        Parameters:
        -----------
        a: parameters of uniform distribution (U(a, b))
        b: parameters of uniform distribution (U(a, b))

        Return:
        --------
        x: random number that satisfied to uniform distribution 
        """
        return a+(b-a)*random.random()

    def exponential(self, beta):
        """
        Generate random number that satisfied to uniform distribution
        
        Parameters:
        -----------
        beta: mean

        Return:
        -------
        x: random number that satisfied to exponential distribution
        """
        return -1.0*beta*math.log(random.random())

    def m_erlang(self, m, beta):
        """
        Generate random number that satisfied to m-Erlang distribution

        Parameters:
        -----------
        m: m
        beta: mean of each exponential distribution

        Return:
        -------
        x: random number that satisfied to m_erlang distribution 
        """
        u = [random.random() for i in range(m)]
        log_u = [math.log(ui) for ui in u]
        return -1.0*beta*sum(log_u)/m

    def gamma(self, alpha, beta):
        """
        Generate random number that satisfied to gamma distribution

        Parameters:
        -----------
        alpha: shape parameter alpha
        beta: inverse scale (rate) parameter beta (beta = 1/theta)

        Return:
        -------
        x: random number that satisfied to gamma distribution
        """
        while 1:
            if (alpha>0) & (alpha<1):
                u1 = random.random()
                b = (math.e + alpha)/math.e
                P = b*u1
                if P>1:
                    Y = -1.0*math.log((b-P)/alpha)
                    u2 = random.random()
                    if u2<= Y**(alpha-1):
                        x = Y
                        break
                    else:
                        continue 
                else:
                    Y = P**(1.0/alpha)
                    u2 = random.random()
                    if u2<=math.log(math.e**(-1.0*Y)):
                        x = Y
                        break
                    else:
                        continue
            elif (alpha > 1):
                a = 1.0/math.sqrt(2*alpha-1)
                b = alpha - math.log(4)
                q = alpha + 1.0/alpha
                theta = 4.5
                d = 1 + math.log(theta)
                u1 = random.random()
                u2 = random.random()
                V = a*math.log(u1/(1-u1))
                Y = alpha*(math.e**V)
                Z = u1*u1*u2
                W = b+q*V-Y
                if W+d-theta*Z >= 0:
                    x = Y
                    break
                else:
                    if W >= math.log(Z):
                        x = Y
                        break
                    else:
                        continue
            elif alpha == 1:
                # Exponential distribution
                x = self.exponential(beta)
                break
            else:
                raise Exception("Wrong range of alpha")
        return x

    def normal(self, mean = 0, std = 1):
        """
        Generate random number that satisfied to gamma distribution

        Parameters:
        -----------
        mean: mean
        std: standard variance

        Return:
        -------
        x1: random number that satisfied to normal distribution
        x2: random number that satisfied to normal distribution
        """
        r1 = random.random()
        r2 = random.random()
        z1 = (-2.0*math.log(r1))**(0.5)*math.cos(2*math.pi*r2)
        z2 = (-2.0*math.log(r2))**(0.5)*math.sin(2*math.pi*r2)
        x1 = mean + std*z1
        x2 = mean + std*z2
        return x1, x2

if __name__ == "__main__":
    sample_number = 10000
    gd_cls = GenDistribution()
    x1 = []
    x2 = []
    for i in range(sample_number):
    # x1~gamma(0.5, 0.5)
        x1.append(gd_cls.gamma(0.5, 0.5))
    # x2~gamma(2, 2)
        x2.append(gd_cls.gamma(2, 2))


