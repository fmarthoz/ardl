import numpy as np

def binary_budget(T, budget=50000,p1=.9,p2=.08,seed=0):
    rng=np.random.default_rng(seed)
    z=np.zeros(T, dtype=int)
    z[0]=rng.integers(0,2)
    for t in range(1,T):
        z[t]=int(rng.random()<(p1 if z[t-1] else p2))
    spend=budget*z
    return spend, z

binary_budget(T=100)

def mean_reverting_budget(T=104,mu=20000,cap=None, seed=0,phi=.8,sigma=1000):
    rng=np.random.default_rng(seed)
    z=np.zeros(T, dtype=int)
    z[0]=mu+rng.normal(0,sigma)
    for t in range(1,T):
        r=rng.normal(0,sigma)
        z[t]=mu+phi*(z[t-1]-mu)+r
    if cap:
        return np.minimum(cap,z)
    else:
        return(z)


def generate_sales_data(*series, betas, intercept=0.0, eps=1e-12):
    X = np.column_stack([np.asarray(s, float).reshape(-1) for s in series])
    beta = np.asarray(betas, float).reshape(-1)
    if X.shape[1] != beta.size:
        raise ValueError("Number of series must match number of betas.")
    # y = exp(intercept) * prod_i x_i**beta_i
    return np.exp(intercept) * np.prod((1+X + eps) ** beta, axis=1)



def add_seasonality(x,amplitude):
    return sales
    
def add_adstock(x):
    sales=0
    return sales

def add_trend(x,p=0.10):
    x=np.array(x)
    T=len(x)
    m=range(T)
    m=m*(x[T-1]*(1+p)-x[T-1])/T
    return m+x

print(add_trend([1,1,1],0.2))
